import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re

# Configurações iniciais
BASE_URL = "https://www.urbes.com.br"
LIST_URL = f"{BASE_URL}/transportes/consulta-horarios"
PRINT_URL_TEMPLATE = BASE_URL + "/comunidade/imprimir/{line_id}"
JSON_FILE = "dados_onibus_sorocaba.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def limpar_texto(texto):
    """
    Remove espaços extras, quebras de linha, tabulações e caracteres especiais como \xa0.
    """
    if not texto:
        return ""
    texto = texto.replace('\xa0', ' ').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    return " ".join(texto.split()).strip()

def fazer_requisicao(url, max_tentativas=5, delay_inicial=2):
    """
    Realiza uma requisição HTTP GET com tratamento de erros, timeouts
    e tentativas automáticas com recuo exponencial (backoff).
    """
    delay = delay_inicial
    for tentativa in range(max_tentativas):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                print(f"   [Aviso] Limite de requisições excedido (HTTP 429). Aguardando {delay}s...")
            else:
                print(f"   [Aviso] Servidor retornou erro HTTP {response.status_code}. Aguardando {delay}s...")
        except requests.exceptions.RequestException as e:
            print(f"   [Aviso] Falha de conexão ({type(e).__name__}) na tentativa {tentativa + 1}/{max_tentativas}. Aguardando {delay}s...")
        
        time.sleep(delay)
        delay *= 2  # Dobra o tempo de espera para a próxima tentativa de conexão
        
    return None

def obter_todas_as_linhas():
    """
    Acede à página principal de horários e extrai o ID e o Nome
    de todas as linhas de autocarro disponíveis no elemento <select>.
    """
    print("A obter a lista de linhas disponíveis no site da URBES...")
    response = fazer_requisicao(LIST_URL)
    if not response or response.status_code != 200:
        raise Exception("Não foi possível acessar a lista de linhas após várias tentativas de conexão.")
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Procura o select que contém as linhas
    select_element = soup.find('select', {'id': 'linha'}) or soup.find('select')
    if not select_element:
        select_element = soup.find('select')
        
    lines = []
    if select_element:
        options = select_element.find_all('option')
        for option in options:
            line_id = option.get('value')
            line_name = option.text.strip()
            if line_id and line_id.isdigit():
                lines.append({
                    "id": line_id,
                    "nome": line_name
                })
    
    print(f"Total de {len(lines)} linhas identificadas.")
    return lines

def raspar_horarios_linha(line_id):
    """
    Acede à versão de impressão da linha e extrai as tabelas de horários,
    itinerários básicos e legendas de rotas adicionais de forma higienizada.
    """
    url = PRINT_URL_TEMPLATE.format(line_id=line_id)
    response = fazer_requisicao(url)
    if not response or response.status_code != 200:
        print(f" [Erro] Não foi possível obter dados para a linha ID {line_id} após várias tentativas.")
        return None
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    dados_linha = {
        "line_id": line_id,
        "itinerarios_legenda": [],
        "tabelas_horarios": {}
    }
    
    # 1. Recolhe textos descritivos e legendas úteis
    legendas = soup.find_all('div', class_='legenda') or soup.find_all('p')
    for leg in legendas:
        texto = limpar_texto(leg.text)
        # CORREÇÃO: Ajustado "palabra" para "palavra" para eliminar o NameError
        if texto and any(palavra in texto for palavra in ["Atende", "Via", "itinerário", "Legenda", "itinerarios"]):
            dados_linha["itinerarios_legenda"].append(texto)
            
    # 2. Localiza e processa as tabelas de horários
    tables = soup.find_all('table')
    labels_padrao = ["Dias Úteis", "Sábados", "Domingos e Feriados"]
    idx_dia = 0
    
    for table in tables:
        rows = table.find_all('tr')
        if not rows:
            continue
            
        # Determina dinamicamente o grupo de dias lendo o conteúdo da tabela
        dia_nome_detectado = None
        for row in rows:
            celulas = row.find_all(['th', 'td'])
            for c in celulas:
                texto_lc = limpar_texto(c.text).lower()
                if "segunda" in texto_lc or "úteis" in texto_lc or "uteis" in texto_lc:
                    dia_nome_detectado = "Dias Úteis"
                    break
                elif "sábado" in texto_lc or "sabado" in texto_lc:
                    dia_nome_detectado = "Sábados"
                    break
                elif "domingo" in texto_lc or "feriado" in texto_lc:
                    dia_nome_detectado = "Domingos e Feriados"
                    break
            if dia_nome_detectado:
                break
                
        if not dia_nome_detectado:
            dia_nome_detectado = labels_padrao[idx_dia] if idx_dia < len(labels_padrao) else f"Tabela_{idx_dia+1}"
            idx_dia += 1
            
        headers_reais = []
        partidas_reais = []
        
        # Filtra e organiza as linhas de dados da tabela
        for row in rows:
            celulas = row.find_all(['th', 'td'])
            textos_celulas = [limpar_texto(c.text) for c in celulas]
            
            # Remove valores totalmente vazios do final da linha
            while textos_celulas and textos_celulas[-1] == "":
                textos_celulas.pop()
                
            if not any(textos_celulas):
                continue
                
            # Verifica se alguma célula possui 'colspan' (comum em banners e títulos de seção da tabela)
            tem_colspan = any(c.has_attr('colspan') and int(c.get('colspan', 1)) > 1 for c in celulas)
            
            # Identifica se é uma linha de metadados decorativos (título de layout)
            e_metadado = tem_colspan
            if not e_metadado:
                for texto in textos_celulas:
                    texto_lc = texto.lower()
                    # Ignora linhas com textos extremamente longos (como parágrafos de ajuda)
                    if len(texto) > 40:
                        e_metadado = True
                        break
                    # Ignora termos típicos de cabeçalhos institucionais repetidos
                    if any(chave in texto_lc for chave in [
                        "tabela impressa", "linha", "plataforma", "ponto", 
                        "horários de", "horario de", "impressão em", "impressao em",
                        "segunda-feira", "sábado", "sabado", "domingo", "feriado",
                        "consulta de horários", "urbes trânsito", "urbes transito",
                        "urbe"
                    ]):
                        e_metadado = True
                        break
                        
            if e_metadado:
                continue
                
            # Verifica se as células contêm apenas horários (ex: "12:30", "08:15(A)", ou vazios "")
            contem_apenas_horarios_ou_vazio = True
            for texto in textos_celulas:
                if texto == "":
                    continue
                e_horario = bool(re.match(r'^\d{1,2}:\d{2}', texto))
                if not e_horario:
                    contem_apenas_horarios_ou_vazio = False
                    break
                    
            if not headers_reais and not contem_apenas_horarios_ou_vazio:
                headers_reais = textos_celulas
            else:
                if any(textos_celulas):
                    partidas_reais.append(textos_celulas)
                    
        # Se nenhuma coluna foi mapeada mas temos partidas, cria colunas genéricas correspondentes ao tamanho
        if not headers_reais and partidas_reais:
            max_colunas = max((len(p) for p in partidas_reais), default=0)
            if max_colunas > 0:
                headers_reais = [f"Coluna {i+1}" for i in range(max_colunas)]
            else:
                headers_reais = []
            
        # Salva apenas se houver dados reais e colunas mapeadas
        if partidas_reais and headers_reais:
            dados_linha["tabelas_horarios"][dia_nome_detectado] = {
                "colunas": headers_reais,
                "partidas": partidas_reais
            }
            
    return dados_linha

def carregar_progresso():
    """
    Carrega o progresso existente se o arquivo já existir, evitando reprocessamento.
    """
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                if isinstance(dados, list):
                    ids_salvos = {str(item["line_id"]) for item in dados if "line_id" in item}
                    return dados, ids_salvos
        except Exception as e:
            print(f"[Aviso] Erro ao ler arquivo existente ({e}). Iniciando um novo arquivo.")
    return [], set()

def salvar_progresso(dados):
    """
    Salva os dados de forma segura usando gravação temporária para evitar corrupção de arquivos.
    """
    try:
        temp_file = JSON_FILE + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        if os.path.exists(JSON_FILE):
            os.remove(JSON_FILE)
        os.rename(temp_file, JSON_FILE)
    except Exception as e:
        print(f"[Erro] Falha ao salvar os dados no arquivo: {e}")

def main():
    try:
        # 1. Carrega dados já coletados anteriormente (se houver)
        resultado_completo, ids_coletados = carregar_progresso()
        if ids_coletados:
            print(f"Progresso detectado: {len(ids_coletados)} linhas já coletadas anteriormente.")
            
        # 2. Busca todas as linhas disponíveis no site
        linhas = obter_todas_as_linhas()
        if not linhas:
            print("Nenhuma linha encontrada. O esquema do site pode ter mudado.")
            return
            
        # Filtra as linhas pendentes
        linhas_pendentes = [l for l in linhas if str(l["id"]) not in ids_coletados]
        total_original = len(linhas)
        total_pendentes = len(linhas_pendentes)
        
        if total_pendentes == 0:
            print("\nTodas as linhas já foram totalmente coletadas com sucesso!")
            return
            
        print(f"\nIniciando raspagem de horários. Total: {total_original} linhas | Restantes: {total_pendentes} linhas.")
        
        # 3. Varre apenas as linhas pendentes
        for i, linha in enumerate(linhas_pendentes):
            line_id = str(linha["id"])
            line_nome = linha["nome"]
            
            print(f"[{i+1}/{total_pendentes}] Processando: {line_nome} (ID: {line_id})...")
            
            detalhes = raspar_horarios_linha(line_id)
            if detalhes:
                detalhes["nome_linha"] = line_nome
                resultado_completo.append(detalhes)
                
                # Salva o progresso imediatamente após cada linha
                salvar_progresso(resultado_completo)
            else:
                print(f"   [Erro] Pulando linha ID {line_id} devido a falhas contínuas de conexão.")
                
            # Intervalo de segurança para respeitar o servidor da URBES
            time.sleep(1.5)
            
        print(f"\nSucesso! Todos os dados disponíveis foram salvos e estruturados em: '{os.path.abspath(JSON_FILE)}'")
            
    except Exception as e:
        print(f"Ocorreu um erro crítico no processo: {e}")

if __name__ == "__main__":
    main()