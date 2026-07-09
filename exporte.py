from openpyxl import Workbook
from Database import buscando_os_produtos

from openpyxl import Workbook

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
        "Marca"
    ])

    
    for produto in produtos:
        ws_produtos.append(produto)

    # ======================
    # Aba Usuários
    # ======================

    # Salvar arquivo
    wb.save("relatorio.xlsx")