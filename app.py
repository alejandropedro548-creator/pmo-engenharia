"""
===========================================================
LIMA ERP

Sistema de Gestão Comercial

Empresa:
Atacadão do Lima

Tecnologia:
Python + Streamlit

Versão:
1.0.0

Descrição:
Sistema comercial desenvolvido para controle de
produtos, estoque, vendas e gestão.
===========================================================
"""


# ==========================================================
# IMPORTAÇÕES
# ==========================================================

import streamlit as st
import pandas as pd
from datetime import date, datetime
from reportlab.pdfgen import canvas
from io import BytesIO


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(

    page_title="LIMA ERP",

    page_icon="🛒",

    layout="wide",

    initial_sidebar_state="expanded"

)



# ==========================================================
# IDENTIDADE VISUAL DO SISTEMA
# ==========================================================


st.markdown(

"""
<style>


/* Fundo principal */

.stApp {

    background-color: #F8FAFC;

}



/* Remove menu padrão */

#MainMenu {

    visibility: hidden;

}


footer {

    visibility: hidden;

}


header {

    visibility: hidden;

}



/* Título */

.titulo {

    font-size: 42px;

    font-weight: 800;

    color: #166534;

}



.subtitulo {

    font-size: 18px;

    color: #475569;

}



/* Cartões */

.card {

    background:white;

    padding:20px;

    border-radius:16px;

    box-shadow:
    0px 4px 15px rgba(0,0,0,0.08);

}



/* Botões */

div.stButton > button {


    width:100%;

    height:45px;

    border-radius:10px;

    background:#15803D;

    color:white;

    font-weight:700;

    border:none;


}



div.stButton > button:hover {


    background:#166534;

    color:white;


}



/* Inputs */

input {

    border-radius:10px !important;

}



</style>

""",

unsafe_allow_html=True

)



# ==========================================================
# BANCO DE DADOS TEMPORÁRIO EM MEMÓRIA
# ==========================================================

# Nesta primeira versão utilizaremos listas e dicionários.
# Posteriormente poderá ser migrado para banco de dados.


if "produtos" not in st.session_state:

    st.session_state.produtos = []



if "vendas" not in st.session_state:

    st.session_state.vendas = []



if "usuario" not in st.session_state:

    st.session_state.usuario = None



if "perfil" not in st.session_state:

    st.session_state.perfil = None



if "autenticado" not in st.session_state:

    st.session_state.autenticado = False



# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================


def gerar_codigo_produto():

    """
    Cria código automático dos produtos.
    """

    numero = len(st.session_state.produtos) + 1

    return f"LIMA-{numero:06d}"




def formatar_moeda(valor):

    """
    Converte número para formato monetário.
    """

    return (

        f"R$ {valor:,.2f}"

        .replace(",", "X")

        .replace(".", ",")

        .replace("X", ".")

    )



# ==========================================================
# CABEÇALHO
# ==========================================================


col1, col2 = st.columns([1,5])



with col1:


    st.image(

        "https://cdn-icons-png.flaticon.com/512/3081/3081559.png",

        width=90

    )



with col2:


    st.markdown(

    """

    <div class="titulo">

    LIMA ERP

    </div>


    <div class="subtitulo">

    Sistema de Gestão Comercial - Atacadão do Lima

    </div>

    """,

    unsafe_allow_html=True

    )



st.divider()
# ==========================================================
# USUÁRIOS DO SISTEMA
# ==========================================================

# Simulação de usuários sem banco de dados.
# Futuramente poderia ser substituído por uma base real.


USUARIOS = {


    "admin": {

        "senha": "1234",

        "nome": "Administrador",

        "perfil": "Administrador"

    },


    "estoque": {

        "senha": "1234",

        "nome": "Funcionário Estoque",

        "perfil": "Funcionário"

    },


    "caixa": {

        "senha": "1234",

        "nome": "Operador de Caixa",

        "perfil": "Caixa"

    }


}



# ==========================================================
# FUNÇÃO DE AUTENTICAÇÃO
# ==========================================================


def autenticar_usuario(usuario, senha):

    """
    Verifica se as credenciais existem.
    Retorna os dados do usuário quando válido.
    """



    if usuario in USUARIOS:


        if USUARIOS[usuario]["senha"] == senha:


            return USUARIOS[usuario]



    return None




# ==========================================================
# TELA DE LOGIN
# ==========================================================


def tela_login():


    st.markdown(

    """

    <div class="card">


    <h2 style="text-align:center;color:#166534;">

    Acesso ao LIMA ERP

    </h2>


    <p style="text-align:center;color:#64748B;">

    Entre com suas credenciais para acessar o sistema.

    </p>


    </div>

    """,

    unsafe_allow_html=True

    )



    st.write("")



    esquerda, centro, direita = st.columns([1,2,1])



    with centro:


        usuario = st.text_input(

            "Usuário"

        )



        senha = st.text_input(

            "Senha",

            type="password"

        )



        entrar = st.button(

            "Entrar no Sistema"

        )



        if entrar:



            dados = autenticar_usuario(

                usuario,

                senha

            )



            if dados:



                st.session_state.usuario = dados["nome"]


                st.session_state.perfil = dados["perfil"]


                st.session_state.autenticado = True



                st.success(

                    "Login realizado com sucesso."

                )


                st.rerun()



            else:



                st.error(

                    "Usuário ou senha incorretos."

                )



# ==========================================================
# MENU DINÂMICO POR PERFIL
# ==========================================================


def criar_menu():


    perfil = st.session_state.perfil



    if perfil == "Administrador":


        paginas = [

            "Dashboard",

            "Cadastro de Produtos",

            "Estoque",

            "Caixa",

            "Painel Gerencial",

            "Sobre Nós"

        ]



    elif perfil == "Funcionário":


        paginas = [

            "Cadastro de Produtos",

            "Estoque",

            "Sobre Nós"

        ]



    else:


        paginas = [

            "Caixa",

            "Sobre Nós"

        ]



    escolha = st.sidebar.radio(

        "Navegação",

        paginas

    )



    return escolha
# ==========================================================
# DASHBOARD INICIAL
# ==========================================================


def dashboard():


    st.markdown(

    f"""

    <h1 style="color:#166534;">

    Bem-vindo, {st.session_state.usuario}

    </h1>


    <p style="color:#64748B;font-size:18px;">

    Visão geral do Atacadão do Lima.

    </p>

    """,

    unsafe_allow_html=True

    )



    st.divider()



    # ======================================================
    # INDICADORES
    # ======================================================


    total_produtos = len(

        st.session_state.produtos

    )



    total_vendas = len(

        st.session_state.vendas

    )



    valor_estoque = 0



    for produto in st.session_state.produtos:


        valor_estoque += (

            produto.get("preco_venda", 0)

            *

            produto.get("quantidade", 0)

        )



    coluna1, coluna2, coluna3 = st.columns(3)



    with coluna1:


        st.markdown(

        f"""

        <div class="card">


        <h4 style="color:#64748B;">

        Produtos cadastrados

        </h4>


        <h2 style="color:#166534;">

        {total_produtos}

        </h2>


        </div>

        """,

        unsafe_allow_html=True

        )



    with coluna2:


        st.markdown(

        f"""

        <div class="card">


        <h4 style="color:#64748B;">

        Vendas realizadas

        </h4>


        <h2 style="color:#166534;">

        {total_vendas}

        </h2>


        </div>

        """,

        unsafe_allow_html=True

        )



    with coluna3:


        st.markdown(

        f"""

        <div class="card">


        <h4 style="color:#64748B;">

        Valor em estoque

        </h4>


        <h2 style="color:#166534;">

        {formatar_moeda(valor_estoque)}

        </h2>


        </div>

        """,

        unsafe_allow_html=True

        )



    st.write("")

    st.divider()



    st.subheader(

        "
# ==========================================================
# CADASTRO DE PRODUTOS
# ==========================================================


def cadastro_produtos():


    st.markdown(

    """

    <h1 style="color:#166534;">

    Cadastro de Produtos

    </h1>


    <p style="color:#64748B;font-size:18px;">

    Registre produtos para controle comercial e estoque.

    </p>

    """,

    unsafe_allow_html=True

    )



    st.divider()



    # ======================================================
    # INFORMAÇÕES BÁSICAS
    # ======================================================


    st.subheader(

        "Informações do Produto"

    )


    coluna1, coluna2 = st.columns(2)



    with coluna1:


        nome = st.text_input(

            "Nome do produto"

        )


        marca = st.text_input(

            "Marca"

        )



    with coluna2:


        categoria = st.selectbox(

            "Categoria",

            [

                "Hortifruti",

                "Açougue",

                "Mercearia",

                "Bebidas",

                "Limpeza",

                "Higiene",

                "Padaria"

            ]

        )


        fornecedor = st.text_input(

            "Fornecedor"

        )



    st.divider()



    # ======================================================
    # VALORES COMERCIAIS
    # ======================================================


    st.subheader(

        "Informações Comerciais"

    )



    coluna3, coluna4 = st.columns(2)



    with coluna3:


        preco_compra = st.number_input(

            "Preço de compra",

            min_value=0.0,

            step=0.50

        )



    with coluna4:


        preco_venda = st.number_input(

            "Preço de venda",

            min_value=0.0,

            step=0.50

        )



    if preco_compra > 0:


        margem = (

            (preco_venda - preco_compra)

            /

            preco_compra

        ) * 100



        st.info(

            f"Margem de lucro estimada: {margem:.2f}%"

        )



    st.divider()



    # ======================================================
    # ESTOQUE
    # ======================================================


    st.subheader(

        "Controle de Estoque"

    )


    coluna5, coluna6 = st.columns(2)



    with coluna5:


        quantidade = st.number_input(

            "Quantidade inicial",

            min_value=0,

            step=1

        )



    with coluna6:


        estoque_minimo = st.number_input(

            "Estoque mínimo",

            min_value=0,

            step=1

        )



    localizacao = st.text_input(

        "Localização no estoque",

        placeholder="Exemplo: Corredor A - Prateleira 02"

    )



    st.divider()



    # ======================================================
    # DATAS
    # ======================================================


    st.subheader(

        "Datas do Produto"

    )


    validade = st.date_input(

        "Data de validade",

        format="DD/MM/YYYY"

    )



    descricao = st.text_area(

        "Descrição"

    )



    st.divider()



    # ======================================================
    # CADASTRAMENTO
    # ======================================================


    if st.button(

        "Cadastrar Produto"

    ):



        if nome.strip() == "":


            st.error(

                "Digite o nome do produto."

            )


            return



        if preco_venda < preco_compra:


            st.warning(

                "Atenção: preço de venda menor que o preço de compra."

            )



        produto = {


            "codigo": gerar_codigo_produto(),


            "nome": nome,


            "marca": marca,


            "categoria": categoria,


            "fornecedor": fornecedor,


            "preco_compra": preco_compra,


            "preco_venda": preco_venda,


            "quantidade": quantidade,


            "estoque_minimo": estoque_minimo,


            "localizacao": localizacao,


            "validade": validade,


            "descricao": descricao,


            "data_cadastro": date.today()

        }



        st.session_state.produtos.append(

            produto

        )



        st.success(

            "Produto cadastrado com sucesso!"

        )



        st.markdown(

        f"""

        ### Resumo do cadastro


        **Código:** {produto['codigo']}


        **Produto:** {produto['nome']}


        **Categoria:** {produto['categoria']}


        **Quantidade:** {produto['quantidade']}


        **Preço venda:** {formatar_moeda(produto['preco_venda'])}


        """

        )
# ==========================================================
# CONTROLE DE ESTOQUE
# ==========================================================


def estoque_produtos():


    st.markdown(

    """

    <h1 style="color:#166534;">

    Controle de Estoque

    </h1>


    <p style="color:#64748B;font-size:18px;">

    Consulte produtos cadastrados e acompanhe níveis de estoque.

    </p>

    """,

    unsafe_allow_html=True

    )



    st.divider()



    produtos = st.session_state.produtos



    if len(produtos) == 0:


        st.info(

            "Nenhum produto cadastrado ainda."

        )


        return




    # ======================================================
    # FILTROS
    # ======================================================


    st.subheader(

        "Filtros"

    )



    coluna1, coluna2 = st.columns(2)



    with coluna1:


        pesquisa = st.text_input(

            "Pesquisar produto"

        )



    with coluna2:


        categorias = list(

            set(

                produto["categoria"]

                for produto in produtos

            )

        )


        categoria_filtro = st.selectbox(

            "Categoria",

            [

                "Todas"

            ] + categorias

        )



    st.divider()



    # ======================================================
    # FILTRAGEM
    # ======================================================


    produtos_filtrados = []



    for produto in produtos:


        nome_ok = (

            pesquisa.lower()

            in

            produto["nome"].lower()

        )


        categoria_ok = (

            categoria_filtro == "Todas"

            or

            produto["categoria"] == categoria_filtro

        )



        if nome_ok and categoria_ok:


            produtos_filtrados.append(produto)




    # ======================================================
    # TABELA
    # ======================================================


    dados = []



    for produto in produtos_filtrados:


        valor_total = (

            produto["preco_venda"]

            *

            produto["quantidade"]

        )


        if produto["quantidade"] <= produto["estoque_minimo"]:


            status = "Estoque baixo"



        else:


            status = "Disponível"




        dados.append(


            {


            "Código":

            produto["codigo"],


            "Produto":

            produto["nome"],


            "Categoria":

            produto["categoria"],


            "Quantidade":

            produto["quantidade"],


            "Preço":

            formatar_moeda(

                produto["preco_venda"]

            ),


            "Valor Estoque":

            formatar_moeda(

                valor_total

            ),


            "Status":

            status


            }


        )



    tabela = pd.DataFrame(dados)



    st.dataframe(

        tabela,

        use_container_width=True,

        hide_index=True

    )



    st.divider()



    # ======================================================
    # ALERTAS
    # ======================================================


    st.subheader(

        "Alertas de Estoque"

    )



    produtos_alerta = []



    for produto in produtos:


        if produto["quantidade"] <= produto["estoque_minimo"]:


            produtos_alerta.append(

                produto

            )



    if len(produtos_alerta) > 0:



        for produto in produtos_alerta:


            st.warning(

                f"""

Produto:

{produto['nome']}


Quantidade atual:

{produto['quantidade']}


Estoque mínimo:

{produto['estoque_minimo']}

                """

            )



    else:


        st.success(

            "Todos os produtos estão com estoque adequado."

        )
# ==========================================================
# ATUALIZAÇÃO DO MENU PRINCIPAL
# ==========================================================


def executar_modulo(pagina):


    """
    Direciona o usuário para
    o módulo selecionado.
    """



    if pagina == "Dashboard":


        dashboard()



    elif pagina == "Cadastro de Produtos":


        cadastro_produtos()



    elif pagina == "Estoque":


        estoque_produtos()



    elif pagina == "Caixa":


        st.markdown(

        """

        <h1 style="color:#166534;">

        Sistema de Caixa

        </h1>


        <p style="color:#64748B;">

        Módulo responsável pelas vendas e emissão de comprovantes.

        </p>

        """,

        unsafe_allow_html=True

        )


        st.info(

            "O módulo Caixa será desenvolvido na próxima etapa."

        )



    elif pagina == "Painel Gerencial":


        st.markdown(

        """

        <h1 style="color:#166534;">

        Painel Gerencial

        </h1>


        <p style="color:#64748B;">

        Indicadores estratégicos para administração.

        </p>

        """,

        unsafe_allow_html=True

        )


        st.info(

            "Os indicadores avançados serão adicionados futuramente."

        )



    elif pagina == "Sobre Nós":


        st.markdown(

        """

        <h1 style="color:#166534;">

        Sobre Nós

        </h1>


        <p style="color:#64748B;font-size:18px;">

        Conheça o Atacadão do Lima.

        </p>

        """,

        unsafe_allow_html=True

        )


        st.info(

            "Página institucional será construída."

        )




# ==========================================================
# EXECUÇÃO FINAL DO SISTEMA
# ==========================================================


if st.session_state.autenticado:


    pagina_atual = criar_menu()


    executar_modulo(

        pagina_atual

    )
# ==========================================================
# SISTEMA DE CAIXA
# ==========================================================


def caixa_vendas():


    st.markdown(

    """

    <h1 style="color:#166534;">

    Sistema de Caixa

    </h1>


    <p style="color:#64748B;font-size:18px;">

    Realize vendas e controle operações comerciais.

    </p>

    """,

    unsafe_allow_html=True

    )



    st.divider()



    if "carrinho" not in st.session_state:


        st.session_state.carrinho = []



    produtos = st.session_state.produtos



    if len(produtos) == 0:


        st.warning(

            "Não existem produtos cadastrados para venda."

        )


        return



    # ======================================================
    # ADICIONAR PRODUTO
    # ======================================================


    st.subheader(

        "Adicionar produtos"

    )



    nomes_produtos = [

        produto["nome"]

        for produto in produtos

    ]



    produto_escolhido = st.selectbox(

        "Produto",

        nomes_produtos

    )



    quantidade = st.number_input(

        "Quantidade",

        min_value=1,

        step=1

    )



    if st.button(

        "Adicionar ao carrinho"

    ):



        produto = next(

            produto

            for produto in produtos

            if produto["nome"] == produto_escolhido

        )



        item = {


            "codigo":

            produto["codigo"],


            "produto":

            produto["nome"],


            "quantidade":

            quantidade,


            "preco":

            produto["preco_venda"],


            "subtotal":

            produto["preco_venda"]

            *

            quantidade

        }



        st.session_state.carrinho.append(

            item

        )


        st.success(

            "Produto adicionado ao carrinho."

        )



    st.divider()



    # ======================================================
    # CARRINHO
    # ======================================================


    st.subheader(

        "Carrinho de compras"

    )



    if len(st.session_state.carrinho) > 0:



        tabela = pd.DataFrame(

            st.session_state.carrinho

        )



        st.dataframe(

            tabela,

            use_container_width=True,

            hide_index=True

        )



        total = sum(

            item["subtotal"]

            for item in st.session_state.carrinho

        )



        st.markdown(

        f"""

        <div class="card">


        <h3>

        Total:

        </h3>


        <h1 style="color:#166534;">

        {formatar_moeda(total)}

        </h1>


        </div>

        """,

        unsafe_allow_html=True

        )



        st.divider()



        # ==================================================
        # FINALIZAÇÃO
        # ==================================================


        st.subheader(

            "Pagamento"

        )



        desconto = st.number_input(

            "Desconto",

            min_value=0.0,

            step=0.50

        )



        forma_pagamento = st.selectbox(

            "Forma de pagamento",

            [

                "Dinheiro",

                "Cartão",

                "PIX"

            ]

        )



        valor_final = total - desconto



        st.info(

            f"Valor final: {formatar_moeda(valor_final)}"

        )



        if st.button(

            "Finalizar venda"

        ):



            venda = {


                "data":

                datetime.now(),


                "produtos":

                st.session_state.carrinho.copy(),


                "desconto":

                desconto,


                "pagamento":

                forma_pagamento,


                "total":

                valor_final

            }



            st.session_state.vendas.append(

                venda

            )



            st.session_state.carrinho = []



            st.success(

                "Venda registrada com sucesso."

            )



            st.rerun()



    else:


        st.info(

            "Carrinho vazio."

        )
# ==========================================================
# FUNÇÕES DE CONTROLE DE ESTOQUE E VENDAS
# ==========================================================


def localizar_produto(codigo):


    """
    Localiza produto pelo código.
    """



    for produto in st.session_state.produtos:


        if produto["codigo"] == codigo:


            return produto



    return None




def atualizar_estoque_venda(carrinho):


    """
    Remove automaticamente os produtos
    vendidos do estoque.
    """



    for item in carrinho:


        produto = localizar_produto(

            item["codigo"]

        )



        if produto:


            produto["quantidade"] -= item["quantidade"]





def validar_estoque(carrinho):


    """
    Verifica se existe quantidade
    suficiente antes da venda.
    """



    for item in carrinho:


        produto = localizar_produto(

            item["codigo"]

        )



        if produto:


            if item["quantidade"] > produto["quantidade"]:


                return False, produto["nome"]



    return True, None




# ==========================================================
# HISTÓRICO DE VENDAS
# ==========================================================


def historico_vendas():


    st.markdown(

    """

    <h1 style="color:#166534;">

    Histórico de Vendas

    </h1>


    <p style="color:#64748B;">

    Consulte todas as vendas realizadas.

    </p>

    """,

    unsafe_allow_html=True

    )



    if len(st.session_state.vendas) == 0:


        st.info(

            "Nenhuma venda registrada."

        )


        return



    dados = []



    for venda in st.session_state.vendas:


        dados.append(

            {


            "Data":

            venda["data"].strftime(

                "%d/%m/%Y %H:%M"

            ),


            "Pagamento":

            venda["pagamento"],


            "Desconto":

            formatar_moeda(

                venda["desconto"]

            ),


            "Total":

            formatar_moeda(

                venda["total"]

            )


            }

        )



    tabela = pd.DataFrame(

        dados

    )



    st.dataframe(

        tabela,

        use_container_width=True,

        hide_index=True

    )



    st.divider()



    faturamento = sum(

        venda["total"]

        for venda in st.session_state.vendas

    )



    st.success(

        f"""

Faturamento acumulado:

{formatar_moeda(faturamento)}

        """

    )
# ==========================================================
# COMPROVANTE DE VENDA
# ==========================================================


def gerar_comprovante(venda):


    """
    Cria um comprovante simples
    da venda realizada.
    """


    comprovante = f"""

================================

        ATACADÃO DO LIMA

          COMPROVANTE

================================


Data:

{venda['data'].strftime('%d/%m/%Y %H:%M')}



Produtos:

"""


    for item in venda["produtos"]:


        comprovante += f"""

{item['produto']}

Quantidade: {item['quantidade']}

Subtotal: {formatar_moeda(item['subtotal'])}


"""



    comprovante += f"""

================================


Desconto:

{formatar_moeda(venda['desconto'])}



Pagamento:

{venda['pagamento']}



TOTAL:

{formatar_moeda(venda['total'])}



================================


Obrigado pela preferência!


"""



    return comprovante





# ==========================================================
# RELATÓRIO DE VENDAS
# ==========================================================


def painel_vendas():


    st.markdown(

    """

    <h1 style="color:#166534;">

    Relatório de Vendas

    </h1>


    <p style="color:#64748B;">

    Análise das vendas realizadas.

    </p>


    """,

    unsafe_allow_html=True

    )



    if len(st.session_state.vendas) == 0:


        st.info(

            "Ainda não existem vendas."

        )


        return



    total_vendas = len(

        st.session_state.vendas

    )


    faturamento = sum(

        venda["total"]

        for venda in st.session_state.vendas

    )



    coluna1, coluna2 = st.columns(2)



    with coluna1:


        st.markdown(

        f"""

        <div class="card">


        <h4>

        Quantidade de vendas

        </h4>


        <h2 style="color:#166534;">

        {total_vendas}

        </h2>


        </div>


        """,

        unsafe_allow_html=True

        )



    with coluna2:


        st.markdown(

        f"""

        <div class="card">


        <h4>

        Faturamento

        </h4>


        <h2 style="color:#166534;">

        {formatar_moeda(faturamento)}

        </h2>


        </div>


        """,

        unsafe_allow_html=True

        )



    st.divider()



    for indice, venda in enumerate(

        st.session_state.vendas,

        start=1

    ):


        with st.expander(

            f"Venda #{indice}"

        ):


            st.text(

                gerar_comprovante(venda)

            )
# ==========================================================
# PAINEL GERENCIAL
# ==========================================================


def painel_gerencial():


    st.markdown(

    """

    <h1 style="color:#166534;">

    Painel Gerencial

    </h1>


    <p style="color:#64748B;font-size:18px;">

    Indicadores estratégicos do Atacadão do Lima.

    </p>


    """,

    unsafe_allow_html=True

    )



    st.divider()



    # ======================================================
    # INDICADORES PRINCIPAIS
    # ======================================================


    total_produtos = len(

        st.session_state.produtos

    )



    valor_estoque = 0



    for produto in st.session_state.produtos:


        valor_estoque += (

            produto["preco_venda"]

            *

            produto["quantidade"]

        )



    faturamento = sum(

        venda["total"]

        for venda in st.session_state.vendas

    )



    quantidade_vendas = len(

        st.session_state.vendas

    )



    coluna1, coluna2, coluna3, coluna4 = st.columns(4)



    with coluna1:


        st.metric(

            "Produtos",

            total_produtos

        )



    with coluna2:


        st.metric(

            "Valor Estoque",

            formatar_moeda(valor_estoque)

        )



    with coluna3:


        st.metric(

            "Vendas",

            quantidade_vendas

        )



    with coluna4:


        st.metric(

            "Faturamento",

            formatar_moeda(faturamento)

        )



    st.divider()



    # ======================================================
    # PRODUTOS POR CATEGORIA
    # ======================================================


    st.subheader(

        "Produtos por Categoria"

    )



    categorias = {}



    for produto in st.session_state.produtos:


        categoria = produto["categoria"]



        if categoria in categorias:


            categorias[categoria] += 1



        else:


            categorias[categoria] = 1




    if categorias:


        grafico_categoria = pd.DataFrame(

            {

            "Categoria":

            list(categorias.keys()),


            "Quantidade":

            list(categorias.values())


            }

        )



        st.bar_chart(

            grafico_categoria,

            x="Categoria",

            y="Quantidade"

        )


    else:


        st.info(

            "Cadastre produtos para gerar gráficos."

        )



    st.divider()



    # ======================================================
    # PRODUTOS MAIS VENDIDOS
    # ======================================================


    st.subheader(

        "Produtos Mais Vendidos"

    )



    vendidos = {}



    for venda in st.session_state.vendas:


        for item in venda["produtos"]:


            nome = item["produto"]



            if nome in vendidos:


                vendidos[nome] += item["quantidade"]



            else:


                vendidos[nome] = item["quantidade"]




    if vendidos:


        ranking = pd.DataFrame(

            {

            "Produto":

            list(vendidos.keys()),


            "Quantidade Vendida":

            list(vendidos.values())


            }

        )


        ranking = ranking.sort_values(

            by="Quantidade Vendida",

            ascending=False

        )



        st.dataframe(

            ranking,

            use_container_width=True,

            hide_index=True

        )



    else:


        st.info(

            "Ainda não existem vendas suficientes."

        )
# ==========================================================
# SOBRE NÓS
# ==========================================================


def sobre_nos():


    st.markdown(

    """

    <h1 style="color:#166534;">

    Atacadão do Lima

    </h1>


    <p style="color:#64748B;font-size:20px;">

    Qualidade, variedade e economia para nossos clientes.

    </p>

    """,

    unsafe_allow_html=True

    )



    st.divider()



    # ======================================================
    # IMAGEM PRINCIPAL
    # ======================================================


    st.image(

        "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d",

        use_container_width=True

    )



    st.markdown(

    """

    ## Quem Somos


    O Atacadão do Lima é uma empresa dedicada ao comércio
    de produtos alimentícios, bebidas, higiene e utilidades.


    Nosso objetivo é oferecer uma experiência completa de compra,
    unindo variedade, organização e preços competitivos.


    """

    )



    st.divider()



    # ======================================================
    # NOSSA ESTRUTURA
    # ======================================================


    st.subheader(

        "Nossa Estrutura"

    )



    coluna1, coluna2 = st.columns(2)



    with coluna1:


        st.image(

            "https://images.unsplash.com/photo-1542838132-92c53300491e",

            use_container_width=True

        )


        st.markdown(

        """

        ### Hortifruti


        Produtos frescos selecionados diariamente
        para garantir qualidade aos clientes.


        """

        )



    with coluna2:


        st.image(

            "https://images.unsplash.com/photo-1556740758-90de374c12ad",

            use_container_width=True

        )


        st.markdown(

        """

        ### Loja Organizada


        Ambiente planejado para facilitar
        a experiência de compra.


        """

        )



    st.divider()



    coluna3, coluna4 = st.columns(2)



    with coluna3:


        st.image(

            "https://images.unsplash.com/photo-1604719312566-8912e9227c6a",

            use_container_width=True

        )


        st.markdown(

        """

        ### Padaria e Produtos Frescos


        Qualidade e variedade para todos os momentos.


        """

        )



    with coluna4:


        st.image(

            "https://images.unsplash.com/photo-1542838132-92c53300491e",

            use_container_width=True

        )


        st.markdown(

        """

        ### Variedade de Produtos


        Um mix completo para atender famílias
        e empresas.


        """

        )



    st.divider()



    # ======================================================
    # COMPROMISSOS
    # ======================================================


    st.subheader(

        "Nosso Compromisso"

    )


    compromissos = [


        "Produtos selecionados com qualidade.",


        "Atendimento próximo ao cliente.",


        "Organização e eficiência operacional.",


        "Melhoria contínua dos serviços."


    ]



    for item in compromissos:


        st.write(

            "✓ " + item

        )



    st.divider()



    # ======================================================
    # CONTATO
    # ======================================================


    st.subheader(

        "Contato"

    )



    st.markdown(

    """

    **Endereço:** Rua das Palmeiras, 245 — Centro Santana de Parnaíba - SP


    **Telefone:** (11) 3456-7890


    **Email:** contato@atacadaodolima.com.br


    """

    )
# ==========================================================
# GERAÇÃO DE NOTA FISCAL / COMPROVANTE PDF
# ==========================================================


def gerar_pdf_venda(venda):


    """
    Gera um comprovante PDF
    da venda realizada.
    """



    buffer = BytesIO()



    pdf = canvas.Canvas(

        buffer

    )



    pdf.setTitle(

        "Comprovante Atacadao do Lima"

    )



    y = 800



    pdf.setFont(

        "Helvetica-Bold",

        16

    )



    pdf.drawString(

        180,

        y,

        "ATACADAO DO LIMA"

    )



    y -= 40



    pdf.setFont(

        "Helvetica",

        12

    )



    pdf.drawString(

        50,

        y,

        "Comprovante de Venda"

    )



    y -= 40



    pdf.drawString(

        50,

        y,

        f"Data: {venda['data'].strftime('%d/%m/%Y %H:%M')}"

    )



    y -= 40



    pdf.drawString(

        50,

        y,

        "Produtos:"

    )



    y -= 25



    for item in venda["produtos"]:



        texto = (

            f"{item['produto']} - "

            f"{item['quantidade']}x - "

            f"{formatar_moeda(item['subtotal'])}"

        )



        pdf.drawString(

            60,

            y,

            texto

        )



        y -= 20




    y -= 20



    pdf.drawString(

        50,

        y,

        f"Desconto: {formatar_moeda(venda['desconto'])}"

    )



    y -= 25



    pdf.drawString(

        50,

        y,

        f"Pagamento: {venda['pagamento']}"

    )



    y -= 25



    pdf.setFont(

        "Helvetica-Bold",

        14

    )



    pdf.drawString(

        50,

        y,

        f"TOTAL: {formatar_moeda(venda['total'])}"

    )



    pdf.save()



    buffer.seek(0)



    return buffer





# ==========================================================
# FINALIZAÇÃO DO SISTEMA
# ==========================================================


def mostrar_pdf_venda(venda):


    arquivo = gerar_pdf_venda(

        venda

    )



    st.download_button(

        label="Baixar comprovante PDF",

        data=arquivo,

        file_name="comprovante_venda.pdf",

        mime="application/pdf"

    )