
def login(page, email, senha):
    try:
        page.get_by_role("link", name=" Signup / Login").click()
        page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address").fill(email)
        page.locator("form").filter(has_text="Login").get_by_placeholder("Password").fill(senha)
        page.get_by_role("button", name="Login").click()
        if page.get_by_text("Your email or password is incorrect!").is_visible():
            return False
        else:
            return True
    except Exception as e:
        print(f"Error occurred while logging in: {e}")
    
def register(page, name, last_name, email, senha, dia, mes, ano, endereco, cidade, estado, cep, numero_telefone, pais):
    try:
        page.get_by_role("textbox", name="Name").fill(name)
        page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address").fill(email)
        page.get_by_role("button", name="Signup").click()
        page.wait_for_load_state("domcontentloaded")
        # Formulario
        page.get_by_role("radio", name="Mr.").check()
        page.get_by_role("textbox", name="Password *").fill(senha)
        page.locator("#days").select_option(dia)
        page.locator("#months").select_option(mes)
        page.locator("#years").select_option(ano)
        page.get_by_role("checkbox", name="Sign up for our newsletter!").check()
        page.get_by_role("checkbox", name="Receive special offers from").check()
        page.get_by_role("textbox", name="First name *").fill(name)
        page.get_by_role("textbox", name="Last name *").fill(last_name)
        page.get_by_role("textbox", name="Address * (Street address, P.").fill(endereco)
        page.get_by_label("Country *").select_option(pais)
        page.get_by_role("textbox", name="State *").fill(estado)
        page.get_by_role("textbox", name="City * Zipcode *").fill(cidade)
        page.locator("#zipcode").fill(cep)
        page.get_by_role("textbox", name="Mobile Number *").fill(numero_telefone)
        page.get_by_role("button", name="Create Account").click()
        
        page.get_by_role("link", name="Continue").click().visible()
        return True
    except Exception as e:
        print(f"Error occurred while registering: {e}")
        return False