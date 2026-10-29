
from datetime import datetime
import sqlite3
import os

# 1. Caminho do banco de dados
pasta = os.path.dirname(__file__)
caminho = os.path.join(pasta, "meu_estoque.db")

estoque = "estoque"

# 2. Cria a tabela se ela ainda não existir
banco = sqlite3.connect(caminho)

banco.execute("""
    CREATE TABLE IF NOT EXISTS estoque (
        id INTEGER PRIMARY KEY,
        nome_do_produto TEXT NOT NULL,
        quantidade INTEGER,
        preco_comprado REAL,
        preco_vendido REAL,
        id_produto INTEGER
    )
""")

banco.commit()
banco.close()


# 3. Conta os produtos
def linhas():
    banco = sqlite3.connect(caminho)

    resultado = banco.execute(
        "SELECT COUNT(*) FROM estoque"
    )
    qtd_itens = resultado.fetchone()[0]

    banco.close()
    return qtd_itens


# 4. Busca os produtos
def dados_estoque():
    banco = sqlite3.connect(caminho)

    resultado = banco.execute("""
        SELECT id, nome_do_produto, quantidade,
               preco_comprado, preco_vendido, id_produto
        FROM estoque
        ORDER BY id
    """)

    lista_do_estoque = resultado.fetchall()

    banco.close()
    return lista_do_estoque


# 5. Adiciona um produto
def adicionar_estoque(nome, qtnd, preco_comprado, preco_vendido,id_produto):
    banco = sqlite3.connect(caminho)

    banco.execute("""
        INSERT INTO estoque (
            nome_do_produto,
            quantidade,
            preco_comprado,
            preco_vendido,
            id_produto
        )
        VALUES (?, ?, ?, ?,?)
    """, (nome, qtnd, preco_comprado, preco_vendido,id_produto))
    banco.commit()
    banco.close()

    print("ADICIONADO AO BANCO COM SUCESSO!")


# 6. Apaga todos os produtos
def apagar_banco():
    banco = sqlite3.connect(caminho)

    banco.execute("DELETE FROM estoque")

    banco.commit()
    banco.close()

    print("TODOS OS ITENS APAGADOS!")


# 7. Apaga um produto pelo ID real
def apagar_dado(linha):
    banco = sqlite3.connect(caminho)

    try:
        # Apaga o produto selecionado
        banco.execute(
            "DELETE FROM estoque WHERE id = ?",
            (linha,)
        )

        # Busca os produtos restantes
        produtos = banco.execute("""
            SELECT nome_do_produto, quantidade,
                   preco_vendido, preco_comprado,id_produto
            FROM estoque
            ORDER BY id
        """).fetchall()

        # Reorganiza os IDs de forma segura dentro da transação
        banco.execute("DELETE FROM estoque")

        for novo_id, produto in enumerate(produtos, start=1):
            nome, quantidade, preco_vendido, preco_comprado,id_produto = produto

            banco.execute("""
                INSERT INTO estoque (
                    id, nome_do_produto, quantidade,
                    preco_vendido, preco_comprado,id_produto
                )
                VALUES (?, ?, ?, ?, ?,?)
            """, (
                novo_id, nome, quantidade,
                preco_vendido, preco_comprado,id_produto
            ))

        banco.commit()
        print("Produto excluído e IDs reorganizados!")

    except Exception:
        banco.rollback()
        raise

    finally:
        banco.close()

# 8. Mostra os produtos numerados na tela
def mostrar_estoque():
    valores = {
            "Soma gastado":0,
            "Valor vendido":0,
            "Faturamento":0
        }
    valorC = 0
    valorV = 0
    produtos = dados_estoque()
    for indice, produto in enumerate(produtos):
        valorC += produto[3]
        valorC = round(valorC,2)
        valorV += produto[4]
        valorV = round(valorV,2)
        print(valorV)
        valores = {
            "Soma gastado":valorC,
            "Valor vendido":valorV,
            "Faturamento":round((valorV-valorC),2)
        }
        print(valores)
    return valores

def buscar_produto(id_produto,quantidade):
    cursor = sqlite3.connect(caminho)
    banco = cursor.cursor()
    banco.execute("SELECT * FROM estoque WHERE id_produto = ?",(id_produto,))
    produto = banco.fetchone()
    print(produto)
    banco.close()
    return produto

def editar(id_produto,quantidade):
    cursor = sqlite3.connect(caminho)
    banco = cursor.cursor()
    banco.execute("SELECT * FROM estoque WHERE id_produto = ?",(id_produto,))
    produto = banco.fetchone()
    tirar = produto[2] - quantidade
    banco.execute(
    "UPDATE estoque SET quantidade = ? WHERE id = ?",
    (tirar,produto[0])
    )
    cursor.commit()
    print(produto)
    banco.close()