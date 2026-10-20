# FATEC_2026 - DASHBOARD

# 🚀 Projetos e Atividades

> Repositório para organizar os projetos, atividades práticas e materiais da disciplina de **DevOps** da FATEC (2026).

Aqui ficam o resumo e a entrega de cada aula, os slides do professor e as pipelines de CI no GitHub Actions que validam os projetos práticos.

---

## 📌 Informações Gerais

- **Disciplina:** DevOps
- **Docente:** Prof. Me. Deivison S. Takatu
- **Integrantes:** Karina Moraes, Mike Franguelli, Nicolly Lemos, Pedro Henrique e Rafaela Mansano
- **Repositório:** https://github.com/mkrosz/FATEC_2026

---

## 📚 Projetos da Disciplina de DevOps

| #  | Aula    | Tema | Entrega | Repositório | Deploy | Tecnologia | Descrição |
| -- | ------- | ---- | ------- | ----------- | ------ | ---------- | --------- |
| 01 | Aula 01 | **Introdução ao DevOps** | [Resumo_aula01.md](DevOps/Aula_01/Resumo_aula01.md) | — | — | Markdown | Resumo da primeira aula |
| 02 | Aula 02 | **Conceitos de CI/CD** | [Documentação (PDF)](DevOps/Aula_02/) | 🔗 [LivrariaDevOps](https://github.com/nicollylemos/LivrariaDevOps) | 🌐 [Ver online](https://livraria-dev-ops.vercel.app/) | HTML / CSS / JS / Vercel | Livraria usando conceitos de DevOps |
| 03 | Aula 03 | **Gerência de Configuração** | [Documentação (PDF)](DevOps/Aula_03/) | 🔗 [ProjetoGitTemplate](https://github.com/nicollylemos/ProjetoGitTemplate) | 🌐 [Ver online](https://projeto-git-template.vercel.app/) | React 18 (react-scripts) | Template de projeto React com boas práticas de Git |
| 04 | Aula 04 | **Ferramentas de CI/CD** | [Aula4_DevOps.md](DevOps/Aula_04/Aula4_DevOps.md) | — | — | Markdown | Comparação entre Azure DevOps, GitHub Actions e outras ferramentas |
| 05 | Aula 05 | **Pipeline de Integração Contínua** | [web-app-medicine](DevOps/Aula_05/web-app-medicine/) | 🔗 [web-app-medicine](https://github.com/caiovfelipe/web-app-medicine) | 🌐 [Ver online](https://caiovfelipe.github.io/web-app-medicine/) | HTML / CSS / JS / GitHub Actions | Pipeline de CI para um webapp de controle de medicamentos |
| 06 | Aula 06 | **Revisão de Ferramentas e Pipelines** | [web-app-medicine](DevOps/Aula_06/) | 🔗 [web-app-medicine](https://github.com/caiovfelipe/web-app-medicine) | 🌐 [Ver online](https://caiovfelipe.github.io/web-app-medicine/) | GitHub Actions | Revisão da pipeline aplicada ao mesmo webapp |
| 07 | Aula 07 | **Testes Automatizados** | [projeto-pipeline-testes](DevOps/Aula_07/projeto-pipeline-testes/) | — | — | React 19 / Vite / Vitest / ESLint | Sistema de descontos com testes unitários, de integração e de performance na pipeline |
| 08 | Aula 08 | **Apresentação de Ferramentas DevOps** | [AWS Cloud Formation (PDF)](DevOps/Aula_08/AWS%20Cloud%20Formation.pdf) | — | — | AWS CloudFormation | Apresentação em grupo sobre infraestrutura como código na AWS |
| 09 | Aula 09 | **Documentação de Software** | [README.md](DevOps/Aula_09/README.md) | 🔗 [setec-publico](https://github.com/mkrosz/setec-publico) | 🌐 [Ver online](https://setecfatec.vercel.app) | Astro / TypeScript / Supabase / Vercel | Documentação completa e README proposto para o site da SETEC |

---

## 📁 Organização do Repositório

```text
📦 FATEC_2026
│
├── 📁 .github/
│   └── workflows/          # Pipelines de CI (GitHub Actions)
│       ├── aula05.yml
│       ├── aula06.yml
│       └── aula07.yml
│
├── 📁 DevOps/
│   ├── Aula_01/            # Resumo da aula
│   ├── Aula_02/            # LivrariaDevOps (repositório externo) + PDF
│   ├── Aula_03/            # ProjetoGitTemplate (repositório externo) + PDF
│   ├── Aula_04/            # Comparativo de ferramentas de CI/CD
│   ├── Aula_05/            # web-app-medicine (cópia do código)
│   ├── Aula_06/            # web-app-medicine (repositório externo)
│   ├── Aula_07/            # projeto-pipeline-testes
│   ├── Aula_08/            # Apresentação AWS CloudFormation
│   ├── Aula_09/            # Documentação do setec-publico
│   └── Material de Aula/   # Slides (PDF) de cada aula
│
└── README.md (you are here!!)
```

---

## ⚙️ Pipelines de CI (GitHub Actions)

Os workflows ficam em [`.github/workflows/`](.github/workflows/) e rodam em `ubuntu-latest` com Node.js 20.

| Workflow | Projeto | Gatilho | Etapas |
| -------- | ------- | ------- | ------ |
| [aula05.yml](.github/workflows/aula05.yml) | `DevOps/Aula_05/web-app-medicine` | push e PR na `main` | checkout → setup Node (cache npm) → `npm ci` → `npm audit` → build → upload do artefato `dist/` |
| [aula06.yml](.github/workflows/aula06.yml) | `DevOps/Aula_06/web-app-medicine` | push na `main` | mesmas etapas da Aula 05 |
| [aula07.yml](.github/workflows/aula07.yml) | `DevOps/Aula_07/projeto-pipeline-testes` | push e PR na `main` | **lint** (ESLint) → **tests** (matriz: unit, integration, performance, com relatórios XML como artefato) → **build** |

Para acompanhar as execuções, abra a aba **Actions** do repositório no GitHub.

---

## 🛠️ Pré-requisitos

| Ferramenta | Versão | Usada em |
| ---------- | ------ | -------- |
| Git | recente | todos |
| Node.js | 20 ou superior | Aulas 03 e 07 (a mesma versão das pipelines) |
| npm | o que vem com o Node | Aulas 03 e 07 |
| Navegador | qualquer navegador moderno | Aulas 02 e 05 (HTML estático) |

---

## ▶️ Como executar os projetos

### 1. Clonar o repositório

```bash
git clone https://github.com/mkrosz/FATEC_2026.git
cd FATEC_2026
```

> ⚠️ As pastas `DevOps/Aula_02/LivrariaDevOps`, `DevOps/Aula_03/ProjetoGitTemplate` e `DevOps/Aula_06/web-app-medicine` são **repositórios externos** e não vêm preenchidas no clone. Para ver o código delas, clone direto pelos links da tabela de projetos.

### 2. Aula 02 e Aula 05 — sites estáticos

Não precisam de instalação: abra o `index.html` no navegador.

- Aula 02: [versão online](https://livraria-dev-ops.vercel.app/) ou clone o [LivrariaDevOps](https://github.com/nicollylemos/LivrariaDevOps).
- Aula 05: `DevOps/Aula_05/web-app-medicine/index.html`.

### 3. Aula 03 — ProjetoGitTemplate (React)

```bash
git clone https://github.com/nicollylemos/ProjetoGitTemplate.git
cd ProjetoGitTemplate
npm install
npm start          # http://localhost:3000
```

### 4. Aula 07 — projeto-pipeline-testes (React + Vite)

```bash
cd DevOps/Aula_07/projeto-pipeline-testes
npm ci
npm run dev                 # servidor de desenvolvimento do Vite (http://localhost:5173)
npm run lint                # ESLint
npm run test:unit           # testes unitários
npm run test:integration    # testes de integração
npm run test:performance    # testes de performance
npm run build               # build de produção em dist/
```

Esses são os mesmos comandos que a pipeline [aula07.yml](.github/workflows/aula07.yml) executa.

### 5. Aula 09 — setec-publico

As instruções completas de instalação, configuração (`.env` do Supabase), execução e deploy estão no [README da Aula 09](DevOps/Aula_09/README.md).

---

## 📖 Material de Aula

Os slides de cada aula ficam em [`DevOps/Material de Aula/`](DevOps/Material%20de%20Aula/):

| Aula | Tema |
| ---- | ---- |
| 01 | Apresentação da Disciplina e Introdução ao DevOps |
| 02 | Conceitos de Integração e Entrega Contínua de Software |
| 03 | Gerência de Configuração |
| 04 | Ferramentas de Integração e Entrega Contínua |
| 05 | Pipeline de Integração Contínua |
| 06 | Revisão Ferramentas e Pipelines |
| 07 | Testes Automatizados |
| 08 | Apresentação Ferramentas DevOps |
| 09 | Documentação de Software |

---

## 🤝 Como contribuir

1. Crie uma pasta `DevOps/Aula_XX/` para a nova aula e coloque nela a entrega (código, `.md` ou PDF).
2. Se o projeto tiver pipeline, crie `.github/workflows/aulaXX.yml` com `working-directory` apontando para a pasta da aula.
3. Faça commits descritivos no padrão `feat:`, `fix:` ou `docs:` (ex.: `feat: adiciona pipeline da Aula 06 para web-app-medicine`).
4. Atualize a tabela de projetos e a estrutura de pastas deste README.

---

## 🔒 O que não versionar

- Arquivos `.env`, senhas, tokens ou chaves de API (ex.: chaves do Supabase da Aula 09).
- A pasta `node_modules/` e os builds (`dist/`, `build/`).
