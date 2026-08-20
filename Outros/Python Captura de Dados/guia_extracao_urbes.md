# Guia Passo a Passo: Extrator de Horários URBES Sorocaba

Este guia descreve como configurar o ambiente, instalar os pacotes necessários, executar o script resiliente **`urbes_scraper.py`** e usufruir do sistema de salvamento incremental (retoma automática) e tratamento de quebras de rede.

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de que tem o **Python 3** instalado no seu computador.


## 🛠️ Passo 1: Preparando a Pasta do Projeto

1. Crie uma pasta específica para o projeto no seu computador (por exemplo, `Python Captura de Dados`).
2. Abra esta pasta no editor de código da sua preferência (como o **VS Code**).

## 📦 Passo 2: Instalando as Dependências

Precisamos de instalar as bibliotecas **`requests`** (para comunicação com o site) e **`beautifulsoup4`** (para analisar o código HTML das tabelas).

1. Abra o terminal integrado do **VS Code**.
2. Execute o comando abaixo para instalar as dependências de uma única vez:

```bash
pip install requests beautifulsoup4 pandas

```

> 💡 **Nota:** Se o comando `pip` não for reconhecido, tente utilizar `pip3` ou `python -m pip install requests beautifulsoup4`.

## ✍️ Passo 3: Criando e Salvando o Arquivo do Script

1. Na raiz do seu projeto, crie um novo ficheiro com o nome exato de **`urbes_scraper.py`**.
2. Copie a última versão do código disponibilizada e cole-a inteiramente dentro deste ficheiro.
3. Guarde o ficheiro (`Ctrl + S` ou `Cmd + S`).

## 🚀 Passo 4: Executando o Coletor

Com o terminal aberto na pasta do seu projeto, digite o seguinte comando e pressione **Enter**:

```bash
python urbes_scraper.py

```

O script iniciará exibindo a contagem total de linhas detectadas no site da **URBES** e iniciará o processamento sequencial de cada uma delas.

## 🛡️ Passo 5: Como funciona a Resiliência contra Quedas de Rede

O script foi blindado contra instabilidades do site ou quedas de ligação de duas maneiras automáticas:

### A. Tentativas Inteligentes (Retry com Backoff)

Caso o site falhe ou a sua internet oscile, o terminal exibirá um aviso amigável. **O script não parará.** Ele tentará refazer a ligação até **5 vezes**, dobrando o tempo de espera a cada nova tentativa para não sobrecarregar o servidor.

### B. Salvamento Incremental (Retoma / Resume)

A cada linha processada com sucesso, os dados são **imediatamente gravados** no ficheiro final **`dados_onibus_sorocaba.json`**.

* Se a sua internet cair por muito tempo ou se fechar o terminal acidentalmente, não se preocupe.
* Basta abrir o terminal e correr `python urbes_scraper.py` novamente. O script lerá o ficheiro `.json` existente, identificará quais linhas já foram descarregadas e **retomará a partir da linha seguinte**, poupando o seu tempo!

## 📂 Passo 6: O Arquivo de Saída dos Dados

Ao final do processamento (ou durante ele), verá um ficheiro chamado **`dados_onibus_sorocaba.json`** na sua pasta. Ele conterá a estrutura limpa de horários e itinerários.

### Exemplo da Estrutura Estruturada dos Dados:

```json
[
    {
        "line_id": "39",
        "nome_linha": "Aldeia dos Laranjais ( 39 )",
        "itinerarios_legenda": [
            "Atende ao Bairro X no sentido Bairro-Centro"
        ],
        "tabelas_horarios": {
            "Dias Úteis": {
                "colunas": [
                    "Bairro",
                    "Terminal"
                ],
                "partidas": [
                    ["05:00", "05:30"],
                    ["06:00", "06:30"]
                ]
            }
        }
    }
]

```
' 
Pronto! Tem agora um **coletor de nível profissional** a correr com total segurança e resiliência na sua máquina.