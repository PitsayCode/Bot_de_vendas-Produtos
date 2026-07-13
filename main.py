from playwright.sync_api import sync_playwright
import auth
import Database
import scraper
import exporte
from dotenv import load_dotenv
import os
load_dotenv()

# IMPORTANTE: O código abaixo é apenas um exemplo de como você pode usar o Playwright para automatizar o login e a coleta de dados de um site. Certifique-se de ter as bibliotecas necessárias instaladas e configure corretamente o ambiente antes de executar o código.

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    page.route("**/*", lambda route: route.abort() if "automationexercise.com" not in route.request.url else route.continue_())
    page.goto("https://automationexercise.com/")
    Database.criar_tabela_produtos()
    Database.criar_tabela_user()
    
    NOME = os.getenv("NAME")
    SOBRENOME = os.getenv("LAST_NAME")
    EMAIL = os.getenv("EMAIL")
    SENHA = os.getenv("SENHA")
    DIA = os.getenv("DIA")
    MES = os.getenv("MES")
    ANO = os.getenv("ANO")
    ENDERECO = os.getenv("ENDERECO")
    CIDADE = os.getenv("CIDADE")
    ESTADO = os.getenv("ESTADO")
    CEP = os.getenv("CEP")
    NUMERO_TELEFONE = os.getenv("NUMERO_TELEFONE")
    PAIS = os.getenv("PAIS")

    Acesso =auth.login(page, EMAIL, SENHA)
    try:
        if Acesso:
            print("Login successful")  
        else:
            user = auth.register(page, NOME, SOBRENOME, EMAIL, SENHA, DIA, MES, ANO, ENDERECO, CIDADE, ESTADO, CEP, NUMERO_TELEFONE, PAIS)
            if user:
                Database.inserir_usuario(
                    name=NOME,
                    last_name=SOBRENOME,
                    email=EMAIL,
                    senha=SENHA,
                    dia=DIA,
                    mes=MES,
                    ano=ANO,
                    endereco=ENDERECO,
                    cidade=CIDADE,
                    estado=ESTADO,
                    cep=CEP,
                    numero_telefone=NUMERO_TELEFONE,
                    pais=PAIS
                )

        dados = scraper.acessar_itens(page)
        for produto in dados:
            Database.inserir_produto(
                    produto=produto[0],
                    preco=produto[1],
                    disponibilidade=produto[2],
                    condicao=produto[3],
                    marca=produto[4]
            )




        exporte.exportar_dados()
        print("Dados exportados com sucesso para relatorio.xlsx")
    except Exception as e:
        print(e)
    
    browser.close()