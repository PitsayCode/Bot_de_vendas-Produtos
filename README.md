# 🤖 Bot de Vendas / Análise de Preços

Robô de automação web construído com **Playwright** que realiza login (ou cadastro) automático no site [Automation Exercise](https://automationexercise.com/), coleta os dados de todos os produtos disponíveis na loja e gera um relatório em Excel com as informações extraídas.

## 📋 O que o robô faz

1. **Autenticação automática** — tenta logar com um usuário de teste; caso o login falhe, preenche todo o formulário de cadastro (nome, endereço, data de nascimento, telefone, etc.) e cria a conta automaticamente.
2. **Persistência de usuário** — salva os dados do usuário cadastrado em um banco SQLite local, evitando duplicidade.
3. **Web scraping de produtos** — navega por todos os produtos da vitrine e extrai:
   - Nome do produto
   - Preço
   - Disponibilidade
   - Condição
   - Marca
4. **Armazenamento em banco de dados** — grava cada produto coletado em uma tabela SQLite (`produtos`).
5. **Exportação para Excel** — gera automaticamente um arquivo `relatorio.xlsx` com todos os produtos coletados, pronto para análise.

## 🗂️ Estrutura do projeto

```
.
├── main.py          # Ponto de entrada: orquestra login/cadastro, scraping, banco e exportação
├── auth.py          # Funções de login e cadastro de usuário via Playwright
├── scraper.py       # Extração dos dados de produtos na página
├── Database.py      # Criação das tabelas e operações no SQLite
├── exporte.py       # Exportação dos dados do banco para um arquivo .xlsx
└── requirements.txt # Dependências do projeto
```

## ⚙️ Tecnologias utilizadas

- [Python 3](https://www.python.org/)
- [Playwright](https://playwright.dev/python/) — automação de navegador
- [SQLite3](https://docs.python.org/3/library/sqlite3.html) — banco de dados local
- [openpyxl](https://openpyxl.readthedocs.io/) — geração de planilhas Excel

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

### 4. Execute o robô

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

- [ ] Adicionar tratamento de erros mais robusto e logging
- [ ] Parametrizar credenciais via variáveis de ambiente (`.env`)
- [ ] Adicionar suporte a múltiplos usuários/execuções agendadas
- [ ] Criar testes automatizados
