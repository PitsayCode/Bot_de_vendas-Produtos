def acessar_itens(page):
    botao = page.get_by_role("link", name=" View Product")
    dados = []
    for view_product in botao.all():
        try:
            view_product.click()
            nome = page.locator(".product-information h2").inner_text()
            preco_antes = page.locator(".product-information span span").inner_text()
            preco = preco_antes.replace("Rs. ", "")  # "500"
            disponibilidade = page.locator(".product-information p:has-text('Availability')").inner_text().split(": ")[1]
            condicao = page.locator(".product-information p:has-text('Condition')").inner_text().split(": ")[1]
            marca = page.locator(".product-information p:has-text('Brand')").inner_text().split(": ")[1]
            dados.append((nome, preco, disponibilidade, condicao, marca))
            
            
            page.go_back()
        except Exception as e:
            print(f"Error occurred while accessing items: {e}")
        
    return dados
