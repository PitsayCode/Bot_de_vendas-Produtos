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
4. **Histórico de preços** — cada execução grava uma **nova linha** por produto coletado na tabela SQLite (`produtos`), com data/hora automática da coleta. Rodando o robô várias vezes, é possível acompanhar a variação de preço de cada produto ao longo do tempo.
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
- [pytest](https://docs.pytest.org/) — testes automatizados

## 🔧 Mudanças da refatoração

Esta versão evoluiu a partir do protótipo inicial, focando em segurança e resiliência da execução:

- **Credenciais fora do código**: email, senha e todos os dados de cadastro (nome, endereço, telefone, etc.) saíram do código-fonte e agora são lidos de um arquivo `.env` via `python-dotenv`, evitando expor dados sensíveis no repositório.
- **Conexões de banco mais seguras**: `Database.py` não mantém mais uma conexão SQLite global aberta durante toda a execução. Cada função abre sua própria conexão (`with sqlite3.connect(...)`) e a fecha explicitamente ao final, evitando conexões penduradas.
- **Histórico de preços**: a tabela `produtos` deixou de ter `UNIQUE` no nome do produto e ganhou uma coluna `data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP`, preenchida automaticamente pelo SQLite a cada `INSERT`. Assim, cada coleta gera uma linha nova (em vez de sobrescrever a anterior), permitindo comparar o preço do mesmo produto em datas diferentes.
- **Coleta resiliente**: em `scraper.py`, o tratamento de erro (`try/except`) agora envolve cada produto individualmente dentro do loop, então uma falha ao extrair um item não interrompe a coleta dos demais.
- **Execução mais robusta**: `main.py` agora envolve o fluxo principal (login/cadastro, scraping, exportação) em um `try/except`, garantindo que o navegador seja fechado corretamente mesmo se algo falhar no meio da execução.
- **Correção no cadastro (`auth.py`)**: `register()` chamava `.click().visible()` após confirmar o cadastro — como `.click()` não retorna nada no Playwright, essa chamada sempre lançava erro e fazia a função retornar `False` mesmo com o cadastro concluído no site. Removida a chamada indevida a `.visible()`.
- **Correção no `inserir_usuario`**: o `INSERT` tinha 13 colunas mas o `VALUES` continha 14 `?`, o que quebrava o cadastro de qualquer usuário novo. Ajustado para 13 `?`, batendo com as colunas.
- **Conversão de tipos**: `preco` agora é convertido para `float` em `scraper.py` no momento da extração, em vez de depender da coerção implícita do SQLite ao gravar uma string numérica.
- **Navegação mais estável**: `page.go_back()` em `scraper.py` passou a usar `wait_until="domcontentloaded"`, evitando timeouts de 30s causados pela espera do evento `"load"` completo (recursos externos lentos no site).
- **Fim da falha em cascata na coleta**: o clique em "View Product" (`scraper.py`) usa `no_wait_after=True`, evitando o mesmo tipo de timeout de 30s do item anterior. Além disso, `page.go_back()` foi movido para um bloco `finally`, garantindo que a página volte para a listagem mesmo quando um produto falha — antes, uma falha nessa etapa deixava a página "presa", fazendo todos os produtos seguintes falharem também.
- **Execução em segundo plano**: `browser = pw.chromium.launch(headless=True)` em `main.py` permite rodar o robô sem abrir janela do navegador, útil para execução em background ou agendada (ver seção [Execução agendada](#-execução-agendada-opcional)). Durante o desenvolvimento/depuração, pode ser útil deixar `headless=False` para acompanhar visualmente o que o robô está fazendo.
- **Banco testável**: todas as funções de `Database.py` agora recebem um parâmetro `db_path='BancoDeDados.db'` (com esse valor como padrão). Isso permite que os testes automatizados usem um banco separado (`teste.db`), sem tocar no banco de dados real.

## 🧪 Testes automatizados

O projeto usa [pytest](https://docs.pytest.org/) para testar as funções de `Database.py` de forma isolada, sem depender do navegador nem do banco de dados real.

```bash
pip install pytest
pytest
```

O `pytest` varre o projeto em busca de arquivos `test_*.py` e executa as funções `test_*` dentro deles. Hoje existe `test_database.py`, cobrindo o fluxo de inserir um produto e conferir que os dados voltam corretos ao consultar. Como esse teste usa um `db_path` próprio (`teste.db`, listado no `.gitignore`), ele nunca mistura dados de teste com o `BancoDeDados.db` real.

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

O robô roda em segundo plano (sem abrir janela do navegador), fará login/cadastro, coletará os produtos e, ao final, o arquivo `relatorio.xlsx` será gerado na raiz do projeto com todos os dados coletados.

## ⏰ Execução agendada (opcional)

Com `headless=True`, o robô não precisa mais de uma janela visível pra rodar, então dá pra automatizar a execução periódica sem precisar disparar `python main.py` manualmente toda vez. Isso **não é configurado no código** — é feito inteiramente pelo agendador de tarefas do sistema operacional, fora do repositório:

**Windows (Agendador de Tarefas):**
1. Abra o **Agendador de Tarefas** e crie uma **Tarefa Básica**.
2. Defina o gatilho (ex: diariamente, a cada X horas).
3. Em "Ação", escolha **Iniciar um programa**:
   - **Programa/script**: caminho do `python.exe` (de preferência o da `venv`, ex: `...\venv\Scripts\python.exe`).
   - **Argumentos**: caminho completo do `main.py`.
   - **Iniciar em**: a pasta raiz do projeto (importante — o script usa caminhos relativos para o `.env`, o `BancoDeDados.db` e o `relatorio.xlsx`).

**Linux/Mac (cron):** adicionar uma linha no `crontab -e` apontando pro Python da `venv` e pro `main.py`, com o `cwd` correto (ou usando `cd` dentro do próprio comando do cron).

Como essa configuração vive no sistema operacional (não em um arquivo do projeto), ela precisa ser refeita em qualquer máquina nova onde o robô for rodar de forma agendada.

## 📊 Saída gerada

- **`BancoDeDados.db`** — banco SQLite com as tabelas `users` e `produtos`. A tabela `produtos` acumula uma linha por coleta (com data/hora), permitindo consultar o histórico de preços de cada item.
- **`relatorio.xlsx`** — planilha com a aba **Produtos**, contendo ID, nome, preço, disponibilidade, condição, marca e data da coleta de cada item.

## 📝 Observações

- O projeto utiliza o site [automationexercise.com](https://automationexercise.com/) como ambiente de testes/demonstração para prática de automação e web scraping.
- O `page.route` em `main.py` bloqueia qualquer requisição que não seja do domínio `automationexercise.com`, otimizando o carregamento da página.
- Este projeto tem fins educacionais, servindo como estudo de automação com Playwright, persistência de dados e geração de relatórios.

## 📌 Próximos passos (ideias de evolução)

- [ ] **Interface para credenciais**: substituir o `.env` fixo por uma interface simples (ou um pop-up) para inserir usuário/senha na hora de rodar, permitindo que outras pessoas usem o robô com suas próprias contas.
- [ ] **Logging estruturado**: trocar os `print()` de erro por um logger de verdade, com níveis (`info`, `warning`, `error`) e, idealmente, gravação em arquivo.
- [ ] **Análise sobre o histórico**: hoje o histórico de preços só é coletado; ainda falta uma forma de comparar/visualizar a variação de preço entre coletas (ex: gráfico, alerta de queda de preço).
- [ ] **Mais cobertura de testes**: hoje só `inserir_produto`/`buscando_os_produtos` têm teste; faltam `criar_tabela_user`, `inserir_usuario` e `buscar_usuario`.

## 🤝 Créditos

Utilizado Claude para criação e ativação do repositório.
