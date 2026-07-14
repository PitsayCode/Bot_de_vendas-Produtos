from openpyxl import Workbook
from Database import buscando_os_produtos

def exportar_dados():

    wb = Workbook()

    # ======================
    # Aba Produtos
    # ======================
    ws_produtos = wb.active
    ws_produtos.title = "Produtos"

    produtos = buscando_os_produtos()

    ws_produtos.append([
        "ID",
        "Produto",
        "Preço",
        "Disponibilidade",
        "Condição",
        "Marca",
        "data"
    ])

    
    for produto in produtos:
        ws_produtos.append(produto)


    # Salvar arquivo
    wb.save("relatorio.xlsx")