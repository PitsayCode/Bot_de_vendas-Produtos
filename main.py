from playwright.sync_api import sync_playwright
import auth
import Database
import scraper
import exporte
# IMPORTANTE: O código abaixo é apenas um exemplo de como você pode usar o Playwright para automatizar o login e a coleta de dados de um site. Certifique-se de ter as bibliotecas necessárias instaladas e configure corretamente o ambiente antes de executar o código.

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    page.route("**/*", lambda route: route.abort() if "automationexercise.com" not in route.request.url else route.continue_())
    page.goto("https://automationexercise.com/")
    Database.criar_tabela_produtos()
    Database.criar_tabela_user()
    
    Acesso =auth.login(page, "jose.silva@example.com", "password123")
    if Acesso:
        print("Login successful")  
    else:
        user = auth.register(page, "jose", "silva", "jose.silva@example.com", "password123", "1", "January", "1990", "456 Oak Ave", "Somewhere", "Somestate", "67890", "555-555-5556", "United States")
        if user:
            Database.inserir_usuario("jose", "silva", "jose.silva@example.com", "password123", "1", "January", "1990", "456 Oak Ave", "Somewhere", "Somestate", "67890", "555-555-5556", "United States")

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
    
    
    browser.close()