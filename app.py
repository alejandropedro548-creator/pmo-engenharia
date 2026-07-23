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
===========================================================
"""


# ==========================================================
# IMPORTAÇÕES
# ==========================================================

import streamlit as st
import pandas as pd
from datetime import datetime, date


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
# IDENTIDADE VISUAL
# ==========================================================

st.markdown(
    """
    <style>

    /* Remove elementos padrões */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }


    /* Fundo */

    .stApp {

        background-color: #F8FAFC;

    }


    /* Títulos */

    .titulo-principal {

        font-size: 42px;

        font-weight: 800;

        color: #166534;

        margin-bottom: 0px;

    }


    .subtitulo {

        font-size: 18px;

        color: #475569;

    }


    /* Cartões */

    .card {

        background-color: white;

        padding: 20px;

        border-radius: 16px;

        box-shadow:
        0px 4px 15px rgba(0,0,0,0.08);

    }


    /* Botões */

    div.stButton > button {

        width: 100%;

        height: 45px;

        border-radius: 10px;

        background-color: #15803D;

        color: white;

        font-weight: 700;

        border: none;

    }


    div.stButton > button:hover {

        background-color: #166534;

        color:white;

    }


    /* Inputs */

    input {

        border-radius: 10px !important;

    }


    /* Separadores */

    hr {

        border: 1px solid #E2E8F0;

    }


    </style>
    """,
    unsafe_allow_html=True
)



# ==========================================================
# SESSION STATE
# ==========================================================

def iniciar_sistema():

    """
    Inicializa todas as estruturas
    utilizadas pelo sistema.
    """


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



iniciar_sistema()



# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================


def gerar_codigo_produto():

    """
    Gera código automático
    para novos produtos.
    """

    quantidade = len(st.session_state.produtos) + 1

    return f"LIMA-{quantidade:06d}"




def formatar_moeda(valor):

    """
    Formata valores monetários.
    """

    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")




# ==========================================================
# CABEÇALHO DO SISTEMA
# ==========================================================


coluna1, coluna2 = st.columns([1,5])


with coluna1:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3081/3081559.png",
        width=90
    )


with coluna2:

    st.markdown(
        """
        <div class="titulo-principal">
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
# SIDEBAR BASE
# ==========================================================


with st.sidebar:


    st.markdown(
        """
        ## LIMA ERP

        Sistema Comercial

        Versão 1.0.0

        """
    )


    st.divider()



    if st.session_state.autenticado:


        st.success(
            f"""
Usuário:

{st.session_state.usuario}

Perfil:

{st.session_state.perfil}
            """
        )


        if st.button("Sair"):

            st.session_state.usuario = None

            st.session_state.perfil = None

            st.session_state.autenticado = False

            st.rerun()



# ==========================================================
# ÁREA PRINCIPAL TEMPORÁRIA
# ==========================================================


if not st.session_state.autenticado:


    st.info(
        """
        Sistema iniciado.

        Próxima etapa:
        implementação da tela de login profissional.
        """
    )


else:


    st.success(
        "Sistema carregado com sucesso."
    )
# ==========================================================
# ÁREA PRINCIPAL TEMPORÁRIA
# ==========================================================
# ==========================================================
# USUÁRIOS DO SISTEMA
# ==========================================================


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
# AUTENTICAÇÃO
# ==========================================================


def autenticar_usuario(usuario, senha):

    """
    Verifica se usuário e senha
    existem no sistema.
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
        Acesso ao Sistema
        </h2>

        <p style="text-align:center;color:#64748B;">
        Entre com suas credenciais para acessar o LIMA ERP
        </p>

        </div>

        """,
        unsafe_allow_html=True
    )


    st.write("")


    coluna1, coluna2, coluna3 = st.columns(
        [1,2,1]
    )


    with coluna2:


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


            dados_usuario = autenticar_usuario(
                usuario,
                senha
            )


            if dados_usuario:


                st.session_state.usuario = dados_usuario["nome"]

                st.session_state.perfil = dados_usuario["perfil"]

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
# MENU DO SISTEMA
# ==========================================================


def menu_usuario():


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
# CONTROLE PRINCIPAL DO SISTEMA
# ==========================================================



if not st.session_state.autenticado:


    tela_login()


else:


    pagina = menu_usuario()



    st.sidebar.divider()


    st.sidebar.caption(

        f"Sessão ativa: {st.session_state.usuario}"

    )


    # ------------------------------------------------------
    # Módulos temporários
    # Serão substituídos pelas funções reais
    # ------------------------------------------------------


        if pagina == "Dashboard":


        # ==================================================
        # DASHBOARD GERENCIAL
        # ==================================================


        st.markdown(
            f"""
            <h1 style="color:#166534;">
            Bem-vindo, {st.session_state.usuario}
            </h1>

            <p style="color:#64748B;font-size:18px;">
            Visão geral do funcionamento do Atacadão do Lima.
            </p>

            """,
            unsafe_allow_html=True
        )



        st.divider()



        # ==================================================
        # CÁLCULO DOS INDICADORES
        # ==================================================


        total_produtos = len(
            st.session_state.produtos
        )


        categorias = []


        for produto in st.session_state.produtos:


            if "categoria" in produto:


                categorias.append(
                    produto["categoria"]
                )


        total_categorias = len(
            set(categorias)
        )



        valor_estoque = 0


        for produto in st.session_state.produtos:


            if "preco_venda" in produto and "quantidade" in produto:


                valor_estoque += (

                    produto["preco_venda"]

                    *

                    produto["quantidade"]

                )




        produtos_vencimento = 0



        # ==================================================
        # CARTÕES PRINCIPAIS
        # ==================================================


        coluna1, coluna2, coluna3, coluna4 = st.columns(4)



        with coluna1:


            st.markdown(
                f"""
                <div class="card">

                <h4 style="color:#64748B;">
                Produtos
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
                Categorias
                </h4>

                <h2 style="color:#166534;">
                {total_categorias}
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
                Valor Estoque
                </h4>

                <h2 style="color:#166534;">
                R$ {valor_estoque:,.2f}
                </h2>

                </div>
                """,
                unsafe_allow_html=True
            )



        with coluna4:


            st.markdown(
                f"""
                <div class="card">

                <h4 style="color:#64748B;">
                Alertas
                </h4>

                <h2 style="color:#CA8A04;">
                {produtos_vencimento}
                </h2>

                </div>
                """,
                unsafe_allow_html=True
            )



        st.write("")

        st.divider()



        # ==================================================
        # GRÁFICO DE CATEGORIAS
        # ==================================================


        st.subheader(
            "Distribuição de Produtos por Categoria"
        )


        if len(st.session_state.produtos) > 0:



            dados_categoria = {}



            for produto in st.session_state.produtos:


                categoria = produto.get(
                    "categoria",
                    "Sem categoria"
                )


                if categoria in dados_categoria:


                    dados_categoria[categoria] += 1


                else:


                    dados_categoria[categoria] = 1




            grafico = pd.DataFrame(

                {

                    "Categoria":

                    list(dados_categoria.keys()),


                    "Quantidade":

                    list(dados_categoria.values())

                }

            )



            st.bar_chart(

                grafico,

                x="Categoria",

                y="Quantidade"

            )



        else:


            st.info(
                "Cadastre produtos para visualizar os indicadores."
            )



        st.divider()



        st.caption(
            "LIMA ERP | Painel Gerencial"
        )



    elif pagina == "Cadastro de Produtos":


        st.title(
            "Cadastro de Produtos"
        )

        st.info(
            "Módulo de cadastro será desenvolvido."
        )



    elif pagina == "Estoque":


        st.title(
            "Controle de Estoque"
        )

        st.info(
            "Módulo de estoque será desenvolvido."
        )



    elif pagina == "Caixa":


        st.title(
            "Sistema de Caixa"
        )

        st.info(
            "Módulo de vendas será desenvolvido."
        )



    elif pagina == "Painel Gerencial":


        st.title(
            "Painel Gerencial"
        )

        st.info(
            "Indicadores e gráficos serão desenvolvidos."
        )



    elif pagina == "Sobre Nós":


        st.title(
            "Sobre Nós"
        )

        st.info(
            "Página institucional será desenvolvida."
        )
