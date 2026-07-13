# 🤖 Bot de Vendas / Análise de Preços

Robô de automação web construído com **Playwright** que realiza login (ou cadastro) automático no site [Automation Exercise](https://automationexercise.com/), coleta os dados de todos os produtos disponíveis na loja e gera um relatório em Excel com as informações extraídas.

## 📋 O que o robô faz

1. **Autenticação automática** — tenta logar com um usuário configurado via variáveis de ambiente; caso o login falhe, preenche todo o formulário de cadastro (nome, endereço, data de nascimento, telefone, etc.) e cria a conta automaticamente.
2. **Persistência de usuário** — salva os dados do usuário cadastrado em um banco SQLite local, evitando duplicidade.
3. **Web scraping de produtos** — navega por todos os produtos da vitrine e extrai:
   - Nome do produto
   - Preço
   - Disponibilidade
   - Condição
   - Marca
4. **Armazenamento em banco de dados** — grava cada produto coletado em uma tabela SQLite (`produtos`). Se o produto já existir, **atualiza o preço e os demais dados** em vez de duplicar ou falhar.
5. **Exportação para Excel** — gera automaticamente um arquivo `relatorio.xlsx` com todos os produtos coletados, pronto para análise.

## 🗂️ Estrutura do projeto

```
.
├── main.py          # Ponto de entrada: orquestra login/cadastro, scraping, banco e exportação
├── auth.py          # Funções de login e cadastro de usuário via Playwright
├── scraper.py       # Extração dos dados de produtos na página
├── Database.py      # Criação das tabelas e operações no SQLite
├── exporte.py       # Exportação dos dados do banco para um arquivo .xlsx
├── .env             # Credenciais e dados de cadastro (não versionado)
└── requirements.txt # Dependências do projeto
```

## ⚙️ Tecnologias utilizadas

- [Python 3](https://www.python.org/)
- [Playwright](https://playwright.dev/python/) — automação de navegador
- [SQLite3](https://docs.python.org/3/library/sqlite3.html) — banco de dados local
- [openpyxl](https://openpyxl.readthedocs.io/) — geração de planilhas Excel
- [python-dotenv](https://pypi.org/project/python-dotenv/) — carregamento de variáveis de ambiente

## 🔧 Mudanças da refatoração

Esta versão evoluiu a partir do protótipo inicial, focando em segurança e resiliência da execução:

- **Credenciais fora do código**: email, senha e todos os dados de cadastro (nome, endereço, telefone, etc.) saíram do código-fonte e agora são lidos de um arquivo `.env` via `python-dotenv`, evitando expor dados sensíveis no repositório.
- **Conexões de banco mais seguras**: `Database.py` não mantém mais uma conexão SQLite global aberta durante toda a execução. Cada função abre sua própria conexão (`with sqlite3.connect(...)`) e a fecha explicitamente ao final, evitando conexões penduradas.
- **Upsert de produtos**: `inserir_produto()` agora usa `INSERT ... ON CONFLICT(produto) DO UPDATE` — ao rodar o robô novamente, um produto já existente tem seu preço e demais dados **atualizados**, em vez de causar um erro de violação de `UNIQUE constraint`.
- **Coleta resiliente**: em `scraper.py`, o tratamento de erro (`try/except`) agora envolve cada produto individualmente dentro do loop, então uma falha ao extrair um item não interrompe a coleta dos demais.
- **Execução mais robusta**: `main.py` agora envolve o fluxo principal (login/cadastro, scraping, exportação) em um `try/except`, garantindo que o navegador seja fechado corretamente mesmo se algo falhar no meio da execução.
- **Correção no cadastro (`auth.py`)**: `register()` chamava `.click().visible()` após confirmar o cadastro — como `.click()` não retorna nada no Playwright, essa chamada sempre lançava erro e fazia a função retornar `False` mesmo com o cadastro concluído no site. Removida a chamada indevida a `.visible()`.
- **Correção no `inserir_usuario`**: o `INSERT` tinha 13 colunas mas o `VALUES` continha 14 `?`, o que quebrava o cadastro de qualquer usuário novo. Ajustado para 13 `?`, batendo com as colunas.
- **Conversão de tipos**: `preco` agora é convertido para `float` em `scraper.py` no momento da extração, em vez de depender da coerção implícita do SQLite ao gravar uma string numérica.
- **Navegação mais estável**: `page.go_back()` em `scraper.py` passou a usar `wait_until="domcontentloaded"`, evitando timeouts de 30s causados pela espera do evento `"load"` completo (recursos externos lentos no site).

## 🚀 Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/PitsayCode/Bot_de_vendas-Produtos.git
cd Bot_de_vendas-Produtos
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
playwright install
```

### 4. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo (os valores de dia/mês/país devem corresponder exatamente às opções do formulário do site, ex: `MES` numérico e `PAIS` por extenso como `United States`):

```
NAME=
LAST_NAME=
EMAIL=
SENHA=
DIA=
MES=
ANO=
ENDERECO=
CIDADE=
ESTADO=
CEP=
NUMERO_TELEFONE=
PAIS=
```

### 5. Execute o robô

```bash
python main.py
```

O navegador será aberto (modo visível), o robô fará login/cadastro, coletará os produtos e, ao final, o arquivo `relatorio.xlsx` será gerado na raiz do projeto com todos os dados coletados.

## 📊 Saída gerada

- **`BancoDeDados.db`** — banco SQLite com as tabelas `users` e `produtos`.
- **`relatorio.xlsx`** — planilha com a aba **Produtos**, contendo ID, nome, preço, disponibilidade, condição e marca de cada item coletado.

## 📝 Observações

- O projeto utiliza o site [automationexercise.com](https://automationexercise.com/) como ambiente de testes/demonstração para prática de automação e web scraping.
- O `page.route` em `main.py` bloqueia qualquer requisição que não seja do domínio `automationexercise.com`, otimizando o carregamento da página.
- Este projeto tem fins educacionais, servindo como estudo de automação com Playwright, persistência de dados e geração de relatórios.

## 📌 Próximos passos (ideias de evolução)

- [ ] **Histórico de preços**: hoje o upsert mantém só o preço mais recente de cada produto; guardar cada coleta com data/hora permitiria analisar variação de preço ao longo do tempo (o objetivo original de um "analisador de preços").
- [ ] **Interface para credenciais**: substituir o `.env` fixo por uma interface simples (ou um pop-up) para inserir usuário/senha na hora de rodar, permitindo que outras pessoas usem o robô com suas próprias contas.
- [ ] **Execução agendada**: rodar em modo `headless=True` e agendar via Task Scheduler/cron para coletas periódicas automáticas.
- [ ] **Logging estruturado**: trocar os `print()` de erro por um logger de verdade, com níveis (`info`, `warning`, `error`) e, idealmente, gravação em arquivo.
- [ ] **Testes automatizados**: cobrir as funções de `Database.py` (schema, upsert) com testes unitários usando um banco SQLite em memória.

## 🤝 Créditos

Utilizado Claude para criação e ativação do repositório.
