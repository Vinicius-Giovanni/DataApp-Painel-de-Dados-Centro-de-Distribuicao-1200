# 📊 DataApp — Painel de Dados com Supabase + Python

> Aplicação web em Python que consulta múltiplas tabelas do Supabase e exibe dashboards com gráficos interativos, construída com Flask, HTML e CSS.

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias e Por Que Cada Uma](#tecnologias-e-por-que-cada-uma)
- [Arquitetura Geral](#arquitetura-geral)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Pré-requisitos](#pré-requisitos)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Configurando o Supabase](#configurando-o-supabase)
- [Como a Aplicação Funciona](#como-a-aplicação-funciona)
- [Funcionalidades](#funcionalidades)
- [Boas Práticas](#boas-práticas)
- [Próximos Passos](#próximos-passos)

---

## 🎯 Sobre o Projeto

O **DataApp** é uma aplicação web voltada para visualização e análise de dados. Ele foi pensado para ser um painel centralizado onde é possível consultar dados armazenados em múltiplas tabelas no Supabase e apresentá-los em forma de gráficos, cards de KPIs e tabelas resumidas, tudo dentro de uma interface web limpa e responsiva.

A ideia principal é manter o projeto simples e direto: o **backend em Python** cuida de toda a lógica de consulta e transformação dos dados, e o **frontend em HTML + CSS** exibe os resultados de forma visual, sem depender de frameworks pesados. Os gráficos são renderizados no navegador via **Chart.js**, uma biblioteca JavaScript leve que recebe os dados processados pelo backend.

Esse tipo de aplicação é ideal para analistas e engenheiros de dados que querem criar painéis customizados sem depender de ferramentas como Power BI ou Metabase, tendo controle total sobre a apresentação e a lógica dos dados.

---

## 🛠️ Tecnologias e Por Que Cada Uma

| Tecnologia | Papel no projeto | Por que essa escolha |
|---|---|---|
| **Python 3.11+** | Linguagem principal | Ecossistema rico para dados, legível e produtivo |
| **Flask** | Servidor web e roteamento | Leve, sem opinião forte, ideal para apps de dados sem complexidade de frontend |
| **Supabase** | Banco de dados (PostgreSQL gerenciado) | API REST pronta, autenticação integrada, painel visual e plano gratuito generoso |
| **supabase-py** | Cliente Python para o Supabase | Abstrai as chamadas HTTP para o Supabase de forma pythônica |
| **Pandas** | Transformação e agregação dos dados | Padrão de mercado para manipulação tabular em Python |
| **HTML5 + CSS3** | Interface do usuário | Controle total do layout sem dependência de frameworks de frontend |
| **Chart.js** | Gráficos interativos | Biblioteca JavaScript leve, sem instalação, carregada via CDN |
| **python-dotenv** | Gerenciamento de variáveis de ambiente | Mantém credenciais fora do código-fonte |

---

## 🏗️ Arquitetura Geral

O projeto segue um fluxo linear e bem separado por responsabilidade:

```
Supabase (PostgreSQL)
        │
        │  supabase-py  →  consultas às tabelas via API REST
        ▼
┌──────────────────────────┐
│      Flask (Backend)     │
│                          │
│  services/   →  acessa e transforma os dados com Pandas
│  controllers/ → decide o que cada rota entrega
│  app.py      →  define as rotas e passa dados aos templates
└────────────┬─────────────┘
             │  dados injetados via Jinja2 (render_template)
             ▼
┌──────────────────────────┐
│   Templates HTML + CSS   │
│   + Chart.js (browser)   │  →  gráficos renderizados no cliente
└──────────────────────────┘
```

O backend nunca envia HTML "montado com gráficos". Ele envia os **dados processados** embutidos nos templates via Jinja2, e o Chart.js no navegador cuida de transformar esses números em visualizações. Isso mantém o servidor leve e o frontend responsável pela camada visual.

---

## 📁 Estrutura de Pastas

```
dataapp/
│
├── app.py                    # Ponto de entrada — inicializa o Flask e registra as rotas
├── config.py                 # Lê as variáveis do .env e centraliza as configurações
├── requirements.txt          # Lista de dependências Python do projeto
├── .env                      # Credenciais reais (jamais versionar)
├── .env.example              # Modelo de variáveis para novos colaboradores
├── .gitignore
│
├── services/                 # Camada de acesso e transformação de dados
│   ├── supabase_client.py    # Inicializa e exporta o cliente Supabase
│   ├── vendas_service.py     # Consultas e agregações da tabela "vendas"
│   └── usuarios_service.py   # Consultas e métricas da tabela "usuarios"
│
├── controllers/              # Lógica de negócio de cada seção da aplicação
│   ├── dashboard_controller.py
│   └── relatorios_controller.py
│
├── static/
│   ├── css/
│   │   ├── style.css         # Estilos globais (navbar, layout base, tipografia)
│   │   └── dashboard.css     # Estilos específicos do painel (cards, gráficos, grid)
│   ├── js/
│   │   └── charts.js         # Configurações e helpers reutilizáveis do Chart.js
│   └── img/
│
└── templates/
    ├── base.html             # Template pai com navbar, footer e imports globais
    ├── index.html            # Página inicial
    ├── dashboard.html        # Dashboard principal
    └── components/
        ├── card.html         # Componente de card de KPI (reutilizável)
        └── chart_block.html  # Bloco de gráfico com título e canvas
```

### Por que separar em `services/` e `controllers/`?

Os **services** são responsáveis exclusivamente por buscar e transformar dados — eles não sabem nada sobre HTTP, rotas ou templates. Se um dia você trocar o Supabase por outro banco, só os services precisam mudar.

Os **controllers** recebem os dados dos services, aplicam regras de negócio (filtros por período, cálculo de variações, formatação de labels) e entregam tudo pronto para a rota renderizar. Isso evita que o `app.py` fique inchado com lógica de dados misturada às rotas.

---

## ✅ Pré-requisitos

- Python **3.11 ou superior**
- `pip` atualizado
- Conta no [Supabase](https://supabase.com) com um projeto criado e tabelas populadas
- Conhecimento básico de Flask e Jinja2

---

## ⚙️ Configuração do Ambiente

O projeto usa **ambiente virtual Python** para isolar as dependências e evitar conflitos com outros projetos na sua máquina. O fluxo é: criar o `venv`, ativá-lo, instalar as dependências via `requirements.txt` e configurar o `.env` com as credenciais do Supabase.

As variáveis necessárias são a **URL do projeto** Supabase, a **chave de acesso** (`anon key` para leitura pública ou `service_role key` para operações privilegiadas no servidor), a `SECRET_KEY` do Flask e a flag de debug para o ambiente de desenvolvimento.

> 💡 Use sempre o `.env.example` como referência ao configurar o projeto em uma nova máquina. Ele documenta quais variáveis são esperadas sem expor valores reais.

---

## 🗄️ Configurando o Supabase

### Estrutura de tabelas

Crie suas tabelas pelo painel do Supabase ou pelo **SQL Editor**. Para cada tabela consultada, defina cuidadosamente os tipos de campo — datas como `DATE` ou `TIMESTAMPTZ`, valores monetários como `NUMERIC`, categorias como `VARCHAR`. Tipagem correta no banco facilita muito as agregações no Pandas e evita conversões manuais.

### Row Level Security (RLS)

O Supabase ativa o **RLS por padrão** em novas tabelas. Isso significa que, mesmo com a `anon key` válida, nenhuma linha será retornada a menos que exista uma política de acesso explícita criada para aquela tabela. Para um painel interno sem autenticação de usuário final, o caminho mais simples é criar uma política que permita leitura pública nas tabelas relevantes diretamente pelo painel do Supabase.

### Qual chave usar?

| Chave | Onde usar | Observação |
|---|---|---|
| `anon` (pública) | Backend Flask para leitura de dados | Respeita o RLS — segura para usar no servidor |
| `service_role` | Backend para operações administrativas | **Nunca** expor no frontend ou em repositórios públicos |

---

## 🔄 Como a Aplicação Funciona

### 1. Consulta ao Supabase

Quando uma rota é acessada pelo navegador, o Flask aciona o **controller** correspondente, que por sua vez chama os **services** necessários. Cada service usa o `supabase-py` para executar uma query na tabela desejada, selecionando apenas as colunas relevantes para aquele contexto, e retorna os dados como uma lista de dicionários Python.

### 2. Transformação com Pandas

Os dados brutos são convertidos em um **DataFrame do Pandas**. A partir daí acontecem os agrupamentos, cálculos de totais e médias, variações percentuais, filtros por data e qualquer outra transformação necessária. O resultado final é um dicionário simples com listas de labels e valores numéricos — estrutura ideal para o Chart.js consumir.

### 3. Renderização com Jinja2

O Flask entrega esse dicionário ao template HTML via `render_template`. O Jinja2 injeta os valores diretamente no bloco JavaScript da página usando o filtro `tojson`, que serializa os dados Python para JSON válido de forma segura. Nenhum dado trafega como string solta — tudo é serializado corretamente.

### 4. Gráficos com Chart.js

No template HTML, o **Chart.js** lê os dados injetados e renderiza os gráficos nos elementos `<canvas>` correspondentes. Cada gráfico tem seu próprio canvas com `id` único, e a configuração (tipo, cores, escalas, labels) fica no bloco de scripts do template — separada da lógica de dados do backend.

---

## ✨ Funcionalidades

- [x] Conexão com Supabase via `supabase-py`
- [x] Consulta e cruzamento de múltiplas tabelas
- [x] Transformação e agregação de dados com Pandas
- [x] Cards de KPIs (totais, médias, contagens)
- [x] Gráfico de Pizza / Donut — distribuição por categoria
- [x] Gráfico de Linha — evolução temporal
- [x] Gráfico de Barras — comparativos entre grupos
- [x] Layout responsivo com CSS Grid
- [x] Tema escuro com variáveis CSS customizadas
- [x] Separação clara entre camadas de dados e apresentação

---

## 📌 Boas Práticas

**Segurança de credenciais**
Nunca coloque a URL ou as chaves do Supabase diretamente no código. Use sempre o `.env` e garanta que ele está no `.gitignore`. A `service_role key` tem acesso irrestrito ao banco — trate-a como senha root.

**Organização do código**
Mantenha os services focados exclusivamente em dados. Se você perceber que está escrevendo lógica de formatação ou apresentação dentro de um service, esse código provavelmente pertence ao controller ou ao template.

**Volume de dados**
O Supabase retorna no máximo 1.000 linhas por padrão em queries sem paginação. Se suas tabelas forem grandes, aplique **filtros de data** diretamente na query ou mova agregações pesadas para **Views ou Funções SQL** no próprio banco, em vez de trazer todos os dados para o Pandas processar no servidor.

**CSS com variáveis**
Use variáveis CSS (`:root`) para cores, espaçamentos e fontes. Isso mantém consistência visual, facilita a criação de temas e evita valores repetidos espalhados pelos arquivos de estilo.

**Dados no frontend**
Sempre use o filtro `tojson` do Jinja2 ao injetar dados Python em blocos `<script>`. Nunca concatene valores diretamente em strings JavaScript — isso é uma brecha de segurança e quebra facilmente com valores que contêm aspas ou caracteres especiais.

---

## 🚀 Próximos Passos

- **Filtros dinâmicos** — selecionar período, categoria ou região via formulário com `fetch` para endpoints internos JSON, sem recarregar a página
- **Endpoints de API internos** — separar rotas que retornam JSON puro (`/api/vendas`) das rotas que retornam HTML, deixando o projeto pronto para integrações futuras
- **Autenticação** — proteger o painel com login usando o **Supabase Auth** integrado ao Flask, controlando quem pode acessar cada dashboard
- **Cache por rota** — evitar re-consultas desnecessárias ao Supabase em dados que mudam pouco, usando `flask-caching` com TTL configurável
- **Aggregations no banco** — mover operações pesadas do Pandas para **Views ou Funções SQL** no Supabase, reduzindo volume de dados trafegados
- **Deploy** — publicar no [Render](https://render.com), [Railway](https://railway.app) ou [Fly.io](https://fly.io) com variáveis de ambiente configuradas pela plataforma, sem `.env` em produção
- **Testes** — cobrir os services com `pytest` usando mock das chamadas ao Supabase para garantir que as transformações de dados estão corretas

---

## 📄 Licença

MIT — livre para usar, modificar e distribuir.