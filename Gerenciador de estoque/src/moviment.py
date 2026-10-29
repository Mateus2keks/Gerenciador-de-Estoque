import os
# Arquivo: processadores/calculador.py

def adicionar_estoque(nome,qtnd,preco_comprado,preco_vendido):
    pasta = os.path.dirname(__file__)
    caminho = os.path.join(pasta,"Logs.txt")
    print("[Calculador] Recebi o dado... Processando...")
    with open(caminho,"a",encoding="utf-8") as arquivo:
        arquivo.write(f"Adicionado {nome,qtnd,preco_comprado,preco_vendido}\n")
    