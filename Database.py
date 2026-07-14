import sqlite3

def criar_tabela_user():
    with sqlite3.connect('BancoDeDados.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            dia INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            endereco TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL,
            cep TEXT NOT NULL,
            numero_telefone TEXT NOT NULL,
            pais TEXT NOT NULL
        );''')
        conn.commit()
    conn.close()

def criar_tabela_produtos():
    with sqlite3.connect('BancoDeDados.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            preco REAL NOT NULL,
            disponibilidade TEXT NOT NULL,
            condicao TEXT NOT NULL,
            marca TEXT NOT NULL,
            data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );''')
        conn.commit()
    conn.close()

def inserir_produto(produto, preco, disponibilidade, condicao, marca):
    with sqlite3.connect('BancoDeDados.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (produto, preco, disponibilidade, condicao, marca)
            VALUES (?, ?, ?, ?, ?)
        ''', (produto, preco, disponibilidade, condicao, marca))
        conn.commit()
    conn.close()

def inserir_usuario(name, last_name, email, senha, dia, mes, ano, endereco, cidade, estado, cep, numero_telefone, pais):
    with sqlite3.connect('BancoDeDados.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
        "SELECT * FROM users WHERE name = ? OR email = ?",
        (name, email)
        )
        user_existente = cursor.fetchone()
        if user_existente is None:
            cursor.execute('''
                INSERT INTO users (name, last_name, email, senha, dia, mes, ano, endereco, cidade, estado, cep, numero_telefone, pais)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, last_name, email, senha, dia, mes, ano, endereco, cidade, estado, cep, numero_telefone, pais))
        conn.commit()
    conn.close()

def buscar_usuario():
    with sqlite3.connect('BancoDeDados.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users;')
        usuarios = cursor.fetchall()
    conn.close()
    return usuarios


def buscando_os_produtos():
    with sqlite3.connect('BancoDeDados.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM produtos;
        ''')
        produtos = cursor.fetchall()
    conn.close()
    return produtos


