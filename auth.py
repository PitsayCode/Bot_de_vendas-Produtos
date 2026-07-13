
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
    
def register(page, NOME, SOBRENOME, EMAIL, SENHA, DIA, MES, ANO, ENDERECO, CIDADE, ESTADO, CEP, NUMERO_TELEFONE, PAIS):
    try:
        page.get_by_role("textbox", name="Name").fill(NOME)
        page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address").fill(EMAIL)
        page.get_by_role("button", name="Signup").click()
        page.wait_for_load_state("domcontentloaded")
        # Formulario
        page.get_by_role("radio", name="Mr.").check()
        page.get_by_role("textbox", name="Password *").fill(SENHA)
        page.locator("#days").select_option(DIA)
        page.locator("#months").select_option(MES)
        page.locator("#years").select_option(ANO)
        page.get_by_role("checkbox", name="Sign up for our newsletter!").check()
        page.get_by_role("checkbox", name="Receive special offers from").check()
        page.get_by_role("textbox", name="First name *").fill(NOME)
        page.get_by_role("textbox", name="Last name *").fill(SOBRENOME)
        page.get_by_role("textbox", name="Address * (Street address, P.").fill(ENDERECO)
        page.get_by_label("Country *").select_option(PAIS)
        page.get_by_role("textbox", name="State *").fill(ESTADO)
        page.get_by_role("textbox", name="City * Zipcode *").fill(CIDADE)
        page.locator("#zipcode").fill(CEP)
        page.get_by_role("textbox", name="Mobile Number *").fill(NUMERO_TELEFONE)
        page.get_by_role("button", name="Create Account").click()
        
        page.get_by_role("link", name="Continue").click().visible()
        return True
    except Exception as e:
        print(f"Error occurred while registering: {e}")
        return False