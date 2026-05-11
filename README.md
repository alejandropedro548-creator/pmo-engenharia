# pmo-engenharia controle de projetos para 
# equipe de engenharia 

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

# ─── CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="INDICADORES DE PROJETOS - PMO ENGENHARIA",
    page_icon="📐",
    layout="wide"
)

# ─── CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f172a; }
    .block-container { padding-top: 1.5rem; }
    h1, h2, h3 { color: #818cf8 !important; }
    .stDataFrame { border-radius: 12px; }
    div[data-testid="metric-container"] {
        background: #1e293b;
        border-radius: 12px;
        padding: 16px;
        border-left: 4px solid #6366f1;
    }
</style>
""", unsafe_allow_html=True)

# ─── DADOS INICIAIS ────────────────────────────────────────
CATEGORIAS = ["Estrutural", "Elétrico", "Hidráulico", "Software", "Infraestrutura", "Ambiental"]
STATUS_OPTS = ["Em andamento", "Concluído", "Atrasado", "Pausado", "Planejado"]
CLASSIFICACOES = ["⭐ Baixa", "⭐⭐ Média", "⭐⭐⭐ Alta", "⭐⭐⭐⭐ Crítica"]
FUNCIONARIOS = ["Ana Silva", "Carlos Melo", "Beatriz Souza", "Ricardo Lima", "Fernanda Costa"]

if "projetos" not in st.session_state:
    st.session_state.projetos = pd.DataFrame([
        {"Projeto": "Reforma Estrutural Bloco A", "Categoria": "Estrutural", "Responsável": "Ana Silva",
         "Progresso (%)": 75, "Status": "Em andamento", "Classificação": "⭐⭐⭐ Alta", "Ano": 2026},
        {"Projeto": "Instalação Elétrica Setor 2", "Categoria": "Elétrico", "Responsável": "Carlos Melo",
         "Progresso (%)": 40, "Status": "Atrasado", "Classificação": "⭐⭐⭐⭐ Crítica", "Ano": 2026},
        {"Projeto": "Sistema de Gestão PMO", "Categoria": "Software", "Responsável": "Beatriz Souza",
         "Progresso (%)": 90, "Status": "Em andamento", "Classificação": "⭐⭐⭐ Alta", "Ano": 2026},
        {"Projeto": "Rede Hidráulica Norte", "Categoria": "Hidráulico", "Responsável": "Ricardo Lima",
         "Progresso (%)": 100, "Status": "Concluído", "Classificação": "⭐⭐ Média", "Ano": 2026},
        {"Projeto": "Pavimentação Acesso Sul", "Categoria": "Infraestrutura", "Responsável": "Fernanda Costa",
         "Progresso (%)": 20, "Status": "Planejado", "Classificação": "⭐ Baixa", "Ano": 2026},
    ])

df = st.session_state.projetos

# ─── HEADER ───────────────────────────────────────────────
st.markdown("## 📐 INDICADORES DE PROJETOS — PMO ENGENHARIA")
st.markdown(f"**Ano de referência: 2026** &nbsp;|&nbsp; Atualizado em: {date.today().strftime('%d/%m/%Y')}")
st.divider()

# ─── ABAS ─────────────────────────────────────────────────
aba1, aba2, aba3 = st.tabs(["📊 Dashboard", "📁 Projetos", "➕ Novo Projeto"])

# ══════════════════════════════════════════════════════════
# ABA 1 — DASHBOARD
# ══════════════════════════════════════════════════════════
with aba1:

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📁 Total de Projetos", len(df))
    col2.metric("✅ Concluídos", len(df[df["Status"] == "Concluído"]))
    col3.metric("⚠️ Atrasados", len(df[df["Status"] == "Atrasado"]))
    col4.metric("📈 Progresso Médio", f"{int(df['Progresso (%)'].mean())}%")

    st.markdown("###")

    col_a, col_b = st.columns(2)

    # Gráfico de barras — Progresso por projeto
    with col_a:
        st.markdown("#### Progresso por Projeto (%)")
        cores = {
            "Concluído": "#10b981",
            "Em andamento": "#6366f1",
            "Atrasado": "#f43f5e",
            "Pausado": "#f59e0b",
            "Planejado": "#64748b"
        }
        df_sorted = df.sort_values("Progresso (%)", ascending=True)
        fig_bar = px.bar(
            df_sorted,
            x="Progresso (%)",
            y="Projeto",
            orientation="h",
            color="Status",
            color_discrete_map=cores,
            range_x=[0, 100],
            height=340
        )
        fig_bar.update_layout(
            plot_bgcolor="#1e293b",
            paper_bgcolor="#1e293b",
            font_color="#e2e8f0",
            legend_title="Status",
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico de pizza — por Categoria
    with col_b:
        st.markdown("#### Projetos por Categoria")
        fig_pie = px.pie(
            df,
            names="Categoria",
            hole=0.45,
            height=340,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(
            plot_bgcolor="#1e293b",
            paper_bgcolor="#1e293b",
            font_color="#e2e8f0",
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Gráfico de barras — por Classificação
    st.markdown("#### Projetos por Classificação")
    class_count = df["Classificação"].value_counts().reset_index()
    class_count.columns = ["Classificação", "Qtd"]
    fig_class = px.bar(
        class_count,
        x="Classificação",
        y="Qtd",
        color="Classificação",
        color_discrete_sequence=["#64748b", "#22d3ee", "#f59e0b", "#f43f5e"],
        height=280
    )
    fig_class.update_layout(
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font_color="#e2e8f0",
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_class, use_container_width=True)

# ══════════════════════════════════════════════════════════
# ABA 2 — PROJETOS
# ══════════════════════════════════════════════════════════
with aba2:
    st.markdown("#### Filtros")
    col_f1, col_f2, col_f3 = st.columns(3)
    filtro_cat = col_f1.multiselect("Categoria", CATEGORIAS, default=CATEGORIAS)
    filtro_status = col_f2.multiselect("Status", STATUS_OPTS, default=STATUS_OPTS)
    filtro_class = col_f3.multiselect("Classificação", CLASSIFICACOES, default=CLASSIFICACOES)

    df_filtrado = df[
        df["Categoria"].isin(filtro_cat) &
        df["Status"].isin(filtro_status) &
        df["Classificação"].isin(filtro_class)
    ]

    st.markdown(f"**{len(df_filtrado)} projeto(s) encontrado(s)**")
    st.divider()

    for i, row in df_filtrado.iterrows():
        cor_status = {
            "Concluído": "🟢", "Em andamento": "🔵",
            "Atrasado": "🔴", "Pausado": "🟡", "Planejado": "⚪"
        }.get(row["Status"], "⚪")

        with st.expander(f"{cor_status} {row['Projeto']} — {row['Progresso (%)']}%"):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Categoria:** {row['Categoria']}")
            c2.markdown(f"**Responsável:** {row['Responsável']}")
            c3.markdown(f"**Ano:** {row['Ano']}")

            c4, c5 = st.columns(2)
            c4.markdown(f"**Status:** {row['Status']}")
            c5.markdown(f"**Classificação:** {row['Classificação']}")

            st.progress(int(row["Progresso (%)"]) / 100, text=f"Progresso: {row['Progresso (%)']}%")

            st.markdown("---")
            col_edit, col_del = st.columns([3, 1])

            with col_edit:
                with st.form(f"edit_{i}"):
                    e1, e2 = st.columns(2)
                    novo_prog = e1.slider("Progresso (%)", 0, 100, int(row["Progresso (%)"]))
                    novo_status = e2.selectbox("Status", STATUS_OPTS, index=STATUS_OPTS.index(row["Status"]))
                    nova_class = st.selectbox("Classificação", CLASSIFICACOES, index=CLASSIFICACOES.index(row["Classificação"]))
                    if st.form_submit_button("💾 Salvar alterações"):
                        st.session_state.projetos.at[i, "Progresso (%)"] = novo_prog
                        st.session_state.projetos.at[i, "Status"] = novo_status
                        st.session_state.projetos.at[i, "Classificação"] = nova_class
                        st.success("Atualizado!")
                        st.rerun()

            with col_del:
                if st.button("🗑️ Remover", key=f"del_{i}"):
                    st.session_state.projetos = st.session_state.projetos.drop(index=i).reset_index(drop=True)
                    st.rerun()

# ══════════════════════════════════════════════════════════
# ABA 3 — NOVO PROJETO
# ══════════════════════════════════════════════════════════
with aba3:
    st.markdown("#### Cadastrar Novo Projeto")
    with st.form("novo_projeto"):
        n1, n2 = st.columns(2)
        nome = n1.text_input("Nome do Projeto")
        categoria = n2.selectbox("Categoria", CATEGORIAS)

        n3, n4 = st.columns(2)
        responsavel = n3.selectbox("Responsável", FUNCIONARIOS)
        ano = n4.number_input("Ano", min_value=2024, max_value=2030, value=2026)

        n5, n6, n7 = st.columns(3)
        progresso = n5.slider("Progresso (%)", 0, 100, 0)
        status = n6.selectbox("Status", STATUS_OPTS)
        classificacao = n7.selectbox("Classificação", CLASSIFICACOES)

        submitted = st.form_submit_button("➕ Cadastrar Projeto")
        if submitted:
            if nome.strip() == "":
                st.error("Digite o nome do projeto!")
            else:
                novo = {
                    "Projeto": nome,
                    "Categoria": categoria,
                    "Responsável": responsavel,
                    "Progresso (%)": progresso,
                    "Status": status,
                    "Classificação": classificacao,
                    "Ano": ano
                }
                st.session_state.projetos = pd.concat(
                    [st.session_state.projetos, pd.DataFrame([novo])],
                    ignore_index=True
                )
                st.success(f"Projeto '{nome}' cadastrado com sucesso!")
                st.rerun()