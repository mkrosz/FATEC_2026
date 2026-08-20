import json
import os

JSON_FILE = "dados_onibus_sorocaba.json"
TXT_OUTPUT = "dados_onibus_sorocaba_kb.txt"

def converter_para_kb():
    if not os.path.exists(JSON_FILE):
        print(f"Erro: O arquivo '{JSON_FILE}' não foi encontrado nesta pasta!")
        return

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        dados = json.load(f)

    texto_final = []

    for item in dados:
        line_id = item.get("line_id", "")
        nome_linha = item.get("nome_linha", "")
        tabelas = item.get("tabelas_horarios", {})

        # Remove o ID do início do nome se ele vier duplicado no scraper (ex: "7 - Industrial Vila Rica" -> "Industrial Vila Rica")
        nome_limpo = nome_linha
        if " - " in nome_linha:
            partes = nome_linha.split(" - ", 1)
            if partes[0].strip().isdigit():
                nome_limpo = partes[1].strip()

        bloco = []
        bloco.append("[LINHA_INICIO]\n")
        bloco.append(f"ID: {line_id}\n")
        bloco.append(f"NOME: {nome_limpo}\n")
        
        # Mapeia e extrai os horários de cada tipo de dia conforme o padrão do exemplo
        for dia_tipo in ["Dias Úteis", "Sábados", "Domingos e Feriados"]:
            tabela = tabelas.get(dia_tipo, {})
            partidas = tabela.get("partidas", [])
            
            horarios_lista = []
            for p in partidas:
                for val in p:
                    val_limpo = val.strip()
                    # Garante que vai capturar apenas os horários válidos formatados
                    if val_limpo and ":" in val_limpo:
                        horarios_lista.append(val_limpo)
            
            if horarios_lista:
                # Transforma o nome do dia para caixa alta e substitui o espaço por underline (DIAS_UTEIS, SABADOS, DOMINGOS_E_FERIADOS)
                tag_dia = dia_tipo.upper().replace(" ", "_").replace("Ú", "U").replace("Á", "A")
                bloco.append(f"{tag_dia}: {', '.join(horarios_lista)}\n")
        
        bloco.append("[LINHA_FIM]")
        texto_final.append("".join(bloco))

    with open(TXT_OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n\n".join(texto_final) + "\n")

    print(f"\nSucesso! Arquivo estruturado para KB gerado em: {os.path.abspath(TXT_OUTPUT)}")
    print("Agora, exclua o arquivo antigo da sua Base de Conhecimento do Botpress e faça o upload deste novo arquivo .txt!")

if __name__ == "__main__":
    converter_para_kb()