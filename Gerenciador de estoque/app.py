#Bibliotecas 
import streamlit as st
import pandas as pd
from src.product import adicionar_estoque, mostrar_estoque,dados_estoque,apagar_dado,linhas, buscar_produto, editar
import os

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    /* Importa as fontes do Google Fonts */
    @import url('https://googleapis.com');

    /* CORRIGIDO: Agora aplica a fonte Changa One que você importou nos títulos */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Changa One', sans-serif !important;
        font-weight: normal !important;
    }
    .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    }

    /* Aplica um negrito encorpado para os textos comuns, botões e inputs */
    html, body, [class*="st-"], p, label, input, button, textarea {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
    }
    div[data-testid="stColumn"]:has(.meu-card) {
        border-radius: 12px !important;
        padding: 16px !important;
        box-shadow: 0px 50px 80px rgba(0, 0, 0, 01) !important;
    }
    /* Remove o fundo e as bordas que o st.container nativo coloca para não duplicar */
    div[data-testid="stColumn"]:has(.meu-card) div[data-testid="stVerticalBlockBorderWrapper"] {
        border: none !important;
        background-color: transparent !important;
        padding:  !important;
    }
    /* Garante que o botão de excluir e o nome fiquem lado a lado */
    .linha-compacta [data-testid="stVerticalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 12px !important;
    }
    /* Ajusta o texto do nome do produto (H4) para não quebrar a linha */
    div[data-testid="stColumn"]:has(.meu-card) h4 {
        color: #CDD6F4 !important;
        margin: 0 !important;
        font-family: 'Changa One', sans-serif !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important; /* Coloca '...' se o nome for gigante */
        font-size: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
linha = mostrar_estoque()
lista_do_estoque = dados_estoque()
quantidade_produto = linhas()
produto_encon = None
t = True
f = False
# Aba de inicio !
if "aba_atual" not in st.session_state:
    st.session_state.aba_atual = "Início"

# 1. CONFIGURAÇÃO DA BARRA LATERAL
with st.sidebar:
    st.title("🌐 Menu")
    # Cria caixas com nomes sobre a aba !
    if st.button("🏠 Início", use_container_width=True):
        st.session_state.aba_atual = "Início"
    if st.button("🏷️ Cadastrar Produto", use_container_width=True):
        st.session_state.aba_atual = "Cadastro"
    if st.button("🔄 Saida",use_container_width=True):
        st.session_state.aba_atual = "Saida"
    if st.button("📦 Estoque", use_container_width=True):
        st.session_state.aba_atual = "Itens em Estoque"     
    if st.button("Sobre", use_container_width=True):
        st.session_state.aba_atual = "Sobre"     

# 2. CONTEÚDO PRINCIPAL (NO MEIO DA TELA)
# Lemos qual é a aba atual salva na memória do site

# - INICIO - Aqui e um guia rapido para cada coisa e uma tela de exebiçao para os itens e informaçoes do estoque
if st.session_state.aba_atual == "Início":

    st.title("🏠 Página Inicial")
    st.write("Conteúdo da página inicial aqui.")

# - CADASTRO - Aqui voce botara os itens que queria adicionar no estoque ! [futuramente tera imagens!!]
elif st.session_state.aba_atual == "Cadastro":
    st.title("📊 Cadastrar Produto")
    st.divider()
    st.subheader("Nome do Produto")
    nome_produto = st.text_input("Nome do produto")

    st.subheader("Quantidade")
    quantidade = st.number_input("Quantidade",step=1)

    st.subheader("Valor Comprado")
    valor_comprado = st.number_input("Comprado",)
    
    st.subheader("Valor Vendido")
    valor_vendido = st.number_input("Vendido")
    
    st.subheader("ID")
    id_produto = int(st.number_input("ID",step=1))

    if st.button("CADASTRAR"):
        st.toast("Produto Cadastrado")
        print(linha)
        adicionar_estoque(nome_produto,quantidade,valor_comprado,valor_vendido,id_produto)

# - SAIDA - Aqui voçe adicionara oq foi saido e salvara os dados disso !
elif st.session_state.aba_atual == "Saida":
    st.title("Saida do Estoque")
    st.subheader("item a tirar")
    c1,c2,c3 = st.columns(3)
    with c1:
        nome = st.text_input("Digite o nome do Produto")
    with c2:
        idd = st.number_input("Digite o Id do Produto",step=1)
    with c3:
        quantidade = st.number_input("Digite a quantidade a tirar",step=1)
    if "a" not in st.session_state:
        st.session_state.confirmando = "a"
    if st.session_state.confirmando == "a":
        if st.button("Ok"):
            produto_encon = buscar_produto(idd,quantidade)
            st.markdown("<hr style='margin: 1px 0;'>",unsafe_allow_html=True)
            st.subheader("Ocorrera essa mudança ?  ")
            #if st.button("enviar"):
            st.session_state.confirmando = "b"
            c1,c2,c3 = st.columns(3)
            with c1:
                 with st.container(border=True):
                     st.subheader(produto_encon[1])
                     st.markdown(f"<hr style='margin: 2px;'>",unsafe_allow_html=True)
                     st.markdown(f"Quantidade Antes {produto_encon[2]}")
            with c2:
                 with st.container():
                     st.subheader("======>")
            with c3:
                 with st.container(border=True):
                     #(2, 'nome', 200, 29.99, 49.99, 213.0)
                     st.subheader(produto_encon[1])
                     st.divider() 
    
            st.markdown("<hr style='margin: 1px 0;'>",unsafe_allow_html=True)
            for a, produto in enumerate(lista_do_estoque):
                 id_banco,nome,quantidade,preco_compra,preco_vendi,id_estoque = produto
                 print(id_estoque)
                 print(produto_encon)
        elif st.session_state.confirmando == "b":
            a = editar(idd,quantidade)
            print('Testeeee')    
# - ESTOQUE - Aqui vc vera algumas informaçoes sobre o estoque 
elif st.session_state.aba_atual == "Itens em Estoque":
    st.title("Produtos do Estoque")
    coluna1, coluna2, coluna3 = st.columns(3,border=True)
    with coluna1:
        st.metric(label="Quantidade de itens no Estoque: ",value=quantidade_produto)
    with coluna2:
        st.metric(label="Valor gasto: ",value=f'R${linha["Soma gastado"]}')
    with coluna3:
        st.metric(label="Faturamento estimado",value=f'R${linha["Faturamento"]}')
    limite = st.number_input("Digite uma Media !",step=1)
    st.divider()

    for i in range(0,len(lista_do_estoque),4):
   
        colunas = st.columns(4)
        grupo = lista_do_estoque[i:i+4]
        for indice, produto in enumerate(grupo):
            id_pro,nome_pro,quanti,preco_compra,preco_vendi,id_pr = produto
            with colunas[indice]:
                with st.container():
                    with st.container():
                        st.markdown("<div class='meu-card'></div>",unsafe_allow_html=True)
                        c,c1 = st.columns(2)
                        with c:
                          st.button("❌ EXCLUIR",key=id_pro,args=(id_pro,),on_click=apagar_dado)
                        with c1:
                            st.markdown(f"<h4>{nome_pro}</h4>",unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 1px 0;'>",unsafe_allow_html=True)
                    if quanti == limite:
                        st.warning(f"Quantidade {quanti}")
                    elif quanti < limite:
                        st.error(f"Quantiade {quanti}")
                    else:
                        st.success(f"Quantidade {quanti}")
                    st.markdown(f"<div style='background-color: rgb(39, 39, 71); padding: 10px; border-radius: 7px;'>PREÇO COMPRADO: R$ {preco_compra}</div>", unsafe_allow_html=True)
                    st.text("")
                    st.markdown(f"<div style='background-color:rgb(48, 54, 56); padding: 10px 10px; border-radius: 7px ;' >PREÇO VENDIDO: R$ {preco_vendi}</div>",unsafe_allow_html=True)
                    st.text("")
                    print("IDS",id_pro)

#  - SOBRE - Aqui é um pouco sobre este sistema e oque ele esta me proporcionando na progamçao e na vida !
elif st.session_state.aba_atual == "Sobre":
    st.title("ℹ️ Informações")
    st.write("Detalhes do sistema criados com botões em bloco.")
    st.markdown("Aqui é um mini sistema de gerenciamento de estoque, Eu criei ele com intuido de praticar minha logica de progamaçao, com essa progama esta elevando ela cada vez mais alto, fazendo eu criar/inventar coisas que eu nunca imaginaria")
    st.markdown("s")
