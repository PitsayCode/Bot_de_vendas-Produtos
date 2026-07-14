import Database

def test_insert_dados():
        caminho_teste = "teste.db"
        Database.criar_tabela_produtos(db_path=caminho_teste)
        Database.inserir_produto("Produto Teste", 99.9, "In Stock", "New", "Marca X", db_path=caminho_teste)

        produtos = Database.buscando_os_produtos(db_path=caminho_teste)

        assert produtos[0][1] == "Produto Teste"