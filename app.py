import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
 
# ─── CONFIG ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PMO Engenharia — Indicadores",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ─── STYLE ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Esconde o menu padrão e rodapé do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
 
    /* Fundo e texto */
    .stApp { background-color: #0d0f14; color: #e8eaf0; }
 
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #14171f;
        border-right: 1px solid rgba(255,255,255,0.07);
    }
 
    /* Cards de KPI */
    .kpi-card {
        background: #14171f;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        text-align: center;
        border-top: 3px solid;
    }
    .kpi-label { font-size: 11px; color: #8b90a0; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { font-size: 2.2rem; font-weight: 700; margin: 8px 0 4px; }
    .kpi-sub   { font-size: 12px; color: #555a6e; }
 
    /* Títulos */
    h1, h2, h3 { color: #e8eaf0 !important; }
 
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #1c2030 !important;
        color: #e8eaf0 !important;
        border: 1px solid rgba(255,255,255,0.13) !important;
        border-radius: 8px !important;
    }
 
    /* Botões */
    .stButton > button {
        background-color: #4f7cff;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
    }
    .stButton > button:hover { background-color: #3d6be8; }
 
    /* Dataframe */
    .stDataFrame { background-color: #14171f; }
 
    /* Divider */
    hr { border-color: rgba(255,255,255,0.07); }
 
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        background-color: #14171f;
        color: #8b90a0;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1c2030;
        color: #e8eaf0;
    }
</style>
""", unsafe_allow_html=True)
 
# ─── DADOS INICIAIS ───────────────────────────────────────────────────────────
DADOS_EXEMPLO = [
    {"Nome": "Expansão Planta Unidade A",    "Categoria": "Infraestrutura",   "Ano": 2023, "Status": "Concluído",    "Classificação": 5, "Progresso": 100, "Responsável": "Carlos Mendes"},
    {"Nome": "Implantação Sistema SCADA",    "Categoria": "Tecnologia",       "Ano": 2024, "Status": "Em Andamento", "Classificação": 4, "Progresso": 65,  "Responsável": "Ana Lima"},
    {"Nome": "Retrofit Subestação Elétrica", "Categoria": "Manutenção",       "Ano": 2024, "Status": "Atrasado",    "Classificação": 2, "Progresso": 30,  "Responsável": "João Silva"},
    {"Nome": "Construção Galpão Logístico",  "Categoria": "Infraestrutura",   "Ano": 2023, "Status": "Concluído",    "Classificação": 4, "Progresso": 100, "Responsável": "Beatriz Costa"},
    {"Nome": "Certificação ISO 9001",        "Categoria": "Qualidade",        "Ano": 2024, "Status": "Em Andamento", "Classificação": 4, "Progresso": 50,  "Responsável": "Marcos Prado"},
    {"Nome": "Melhoria Eficiência Energética","Categoria":"Sustentabilidade", "Ano": 2023, "Status": "Concluído",    "Classificação": 5, "Progresso": 100, "Responsável": "Lúcia Ferreira"},
    {"Nome": "Novo ERP Corporativo",         "Categoria": "Tecnologia",       "Ano": 2025, "Status": "Planejado",   "Classificação": 3, "Progresso": 0,   "Responsável": "Rafael Melo"},
    {"Nome": "Plano de Segurança Ocupacional","Categoria":"Segurança",        "Ano": 2024, "Status": "Em Andamento", "Classificação": 5, "Progresso": 80,  "Responsável": "Fabiana Torres"},
    {"Nome": "Modernização Linha de Produção","Categoria":"Infraestrutura",   "Ano": 2025, "Status": "Planejado",   "Classificação": 3, "Progresso": 5,   "Responsável": "Diego Alves"},
    {"Nome": "Programa Lean Manufacturing",  "Categoria": "Qualidade",        "Ano": 2023, "Status": "Concluído",    "Classificação": 4, "Progresso": 100, "Responsável": "Priya Nair"},
]
 
STATUS_CORES = {
    "Concluído":    "#2dd4a0",
    "Em Andamento": "#4f7cff",
    "Atrasado":     "#f05c5c",
    "Planejado":    "#8b90a0",
    "Pausado":      "#f0964a",
    "Cancelado":    "#a78bfa",
}
 
CATEGORIAS_PADRAO = [
    "Infraestrutura", "Tecnologia", "Manutenção", "Qualidade",
    "Sustentabilidade", "Segurança", "Financeiro", "RH", "Outro"
]
 
# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "projetos" not in st.session_state:
    st.session_state.projetos = pd.DataFrame(DADOS_EXEMPLO)
 
if "editando_idx" not in st.session_state:
    st.session_state.editando_idx = None
 
 
# ─── FUNÇÕES AUXILIARES ───────────────────────────────────────────────────────
def estrelas(n):
    return "⭐" * int(n) + "☆" * (5 - int(n))
 
def get_df_filtrado(df, filtro_ano, filtro_cat, filtro_status, busca):
    mask = pd.Series([True] * len(df), index=df.index)
    if filtro_ano != "Todos":
        mask &= df["Ano"] == int(filtro_ano)
    if filtro_cat != "Todas":
        mask &= df["Categoria"] == filtro_cat
    if filtro_status != "Todos":
        mask &= df["Status"] == filtro_status
    if busca:
        q = busca.lower()
        mask &= (
            df["Nome"].str.lower().str.contains(q, na=False) |
            df["Categoria"].str.lower().str.contains(q, na=False) |
            df["Responsável"].str.lower().str.contains(q, na=False)
        )
    return df[mask].copy()
 
 
# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 PMO Engenharia")
    st.markdown("**Indicadores de Projetos**")
    st.divider()
 
    st.markdown("### 🔍 Filtros")
    df = st.session_state.projetos
 
    anos = ["Todos"] + sorted(df["Ano"].unique().tolist(), reverse=True) if len(df) > 0 else ["Todos"]
    filtro_ano = st.selectbox("Ano", anos)
 
    cats = ["Todas"] + sorted(df["Categoria"].unique().tolist()) if len(df) > 0 else ["Todas"]
    filtro_cat = st.selectbox("Categoria", cats)
 
    statuses = ["Todos"] + sorted(df["Status"].unique().tolist()) if len(df) > 0 else ["Todos"]
    filtro_status = st.selectbox("Status", statuses)
 
    busca = st.text_input("🔎 Buscar projeto...")
 
    st.divider()
 
    # Contagem por status na sidebar
    if len(df) > 0:
        st.markdown("### 📌 Por Status")
        for s, cor in STATUS_CORES.items():
            cnt = len(df[df["Status"] == s])
            if cnt > 0:
                st.markdown(f"<span style='color:{cor}'>●</span> **{s}**: {cnt}", unsafe_allow_html=True)
 
    st.divider()
 
    # Importar CSV
    st.markdown("### 📥 Importar CSV")
    uploaded = st.file_uploader("Carregar CSV", type=["csv"])
    if uploaded:
        try:
            df_import = pd.read_csv(uploaded)
            cols_req = {"Nome","Categoria","Ano","Status","Classificação","Progresso","Responsável"}
            if cols_req.issubset(set(df_import.columns)):
                st.session_state.projetos = df_import
                st.success("✅ Importado com sucesso!")
                st.rerun()
            else:
                st.error(f"CSV precisa ter as colunas: {cols_req}")
        except Exception as e:
            st.error(f"Erro ao ler CSV: {e}")
 
 
# ─── CONTEÚDO PRINCIPAL ───────────────────────────────────────────────────────
st.markdown("# 📊 PMO Engenharia — Indicadores de Projetos")
 
df = st.session_state.projetos
df_f = get_df_filtrado(df, filtro_ano, filtro_cat, filtro_status, busca)
 
# ─── TABS ─────────────────────────────────────────────────────────────────────
tab_dash, tab_projetos, tab_add = st.tabs(["📈 Dashboard", "📋 Projetos", "➕ Novo / Editar Projeto"])
 
 
# ══════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════
with tab_dash:
    if len(df_f) == 0:
        st.info("Nenhum projeto encontrado com os filtros selecionados.")
    else:
        # KPI CARDS
        total   = len(df_f)
        concl   = len(df_f[df_f["Status"] == "Concluído"])
        andamen = len(df_f[df_f["Status"] == "Em Andamento"])
        atras   = len(df_f[df_f["Status"] == "Atrasado"])
        pct     = round(concl / total * 100) if total else 0
        avg_cl  = round(df_f["Classificação"].mean(), 1) if total else 0
 
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown(f"""<div class="kpi-card" style="border-top-color:#4f7cff">
                <div class="kpi-label">Total de Projetos</div>
                <div class="kpi-value" style="color:#4f7cff">{total}</div>
                <div class="kpi-sub">cadastrados</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="kpi-card" style="border-top-color:#2dd4a0">
                <div class="kpi-label">Concluídos</div>
                <div class="kpi-value" style="color:#2dd4a0">{concl}</div>
                <div class="kpi-sub">{pct}% do total</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="kpi-card" style="border-top-color:#4f7cff">
                <div class="kpi-label">Em Andamento</div>
                <div class="kpi-value" style="color:#4f7cff">{andamen}</div>
                <div class="kpi-sub">projetos ativos</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="kpi-card" style="border-top-color:#f05c5c">
                <div class="kpi-label">Atrasados</div>
                <div class="kpi-value" style="color:#f05c5c">{atras}</div>
                <div class="kpi-sub">requerem atenção</div>
            </div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""<div class="kpi-card" style="border-top-color:#f5c842">
                <div class="kpi-label">Nota Média</div>
                <div class="kpi-value" style="color:#f5c842">{avg_cl}</div>
                <div class="kpi-sub">classificação ⭐</div>
            </div>""", unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
 
        # LINHA 1 DE GRÁFICOS
        col_a, col_b = st.columns(2)
 
        with col_a:
            st.markdown("##### Status por Categoria")
            df_cat = df_f.groupby(["Categoria","Status"]).size().reset_index(name="Quantidade")
            fig_bar = px.bar(
                df_cat, x="Categoria", y="Quantidade", color="Status",
                color_discrete_map=STATUS_CORES,
                template="plotly_dark",
                barmode="stack",
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#8b90a0", showlegend=True,
                legend=dict(orientation="h", y=1.1, font=dict(size=10)),
                margin=dict(l=0,r=0,t=30,b=0), height=280,
            )
            fig_bar.update_xaxes(gridcolor="rgba(255,255,255,0.05)")
            fig_bar.update_yaxes(gridcolor="rgba(255,255,255,0.05)", dtick=1)
            st.plotly_chart(fig_bar, use_container_width=True)
 
        with col_b:
            st.markdown("##### Distribuição por Status")
            df_status = df_f["Status"].value_counts().reset_index()
            df_status.columns = ["Status","Quantidade"]
            fig_donut = px.pie(
                df_status, names="Status", values="Quantidade",
                color="Status", color_discrete_map=STATUS_CORES,
                hole=0.55, template="plotly_dark",
            )
            fig_donut.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#8b90a0",
                legend=dict(orientation="h", y=-0.1, font=dict(size=10)),
                margin=dict(l=0,r=0,t=20,b=0), height=280,
            )
            fig_donut.update_traces(textinfo="label+percent", textfont_color="#e8eaf0")
            st.plotly_chart(fig_donut, use_container_width=True)
 
        # LINHA 2 DE GRÁFICOS
        col_c, col_d = st.columns(2)
 
        with col_c:
            st.markdown("##### Projetos por Ano")
            df_ano = df_f.groupby(["Ano","Status"]).size().reset_index(name="Quantidade")
            fig_line = px.line(
                df_ano, x="Ano", y="Quantidade", color="Status",
                color_discrete_map=STATUS_CORES,
                markers=True, template="plotly_dark",
            )
            fig_line.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#8b90a0",
                legend=dict(orientation="h", y=1.1, font=dict(size=10)),
                margin=dict(l=0,r=0,t=30,b=0), height=260,
            )
            fig_line.update_xaxes(gridcolor="rgba(255,255,255,0.05)", dtick=1)
            fig_line.update_yaxes(gridcolor="rgba(255,255,255,0.05)", dtick=1)
            st.plotly_chart(fig_line, use_container_width=True)
 
        with col_d:
            st.markdown("##### Progresso Médio por Categoria")
            df_prog = df_f.groupby("Categoria")["Progresso"].mean().reset_index()
            df_prog.columns = ["Categoria", "Progresso Médio (%)"]
            df_prog = df_prog.sort_values("Progresso Médio (%)", ascending=True)
            fig_hbar = px.bar(
                df_prog, x="Progresso Médio (%)", y="Categoria",
                orientation="h", template="plotly_dark",
                color="Progresso Médio (%)",
                color_continuous_scale=["#f05c5c","#f5c842","#2dd4a0"],
                range_color=[0,100],
            )
            fig_hbar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#8b90a0", showlegend=False,
                coloraxis_showscale=False,
                margin=dict(l=0,r=0,t=10,b=0), height=260,
            )
            fig_hbar.update_xaxes(gridcolor="rgba(255,255,255,0.05)", range=[0,105])
            fig_hbar.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
            st.plotly_chart(fig_hbar, use_container_width=True)
 
        # SCATTER — Classificação vs Progresso
        st.markdown("##### Classificação vs. Progresso")
        fig_sc = px.scatter(
            df_f, x="Progresso", y="Classificação",
            color="Status", size_max=14,
            color_discrete_map=STATUS_CORES,
            hover_name="Nome",
            hover_data={"Categoria":True,"Ano":True,"Responsável":True},
            template="plotly_dark",
        )
        fig_sc.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#8b90a0",
            legend=dict(orientation="h", y=1.05, font=dict(size=10)),
            margin=dict(l=0,r=0,t=30,b=0), height=300,
        )
        fig_sc.update_xaxes(gridcolor="rgba(255,255,255,0.05)", title="Progresso (%)", range=[-5,105])
        fig_sc.update_yaxes(gridcolor="rgba(255,255,255,0.05)", title="Classificação ⭐", range=[0.5,5.5], dtick=1)
        fig_sc.update_traces(marker=dict(size=12, opacity=0.85))
        st.plotly_chart(fig_sc, use_container_width=True)
 
 
# ══════════════════════════════════════════════════════════════
# TAB 2 — PROJETOS
# ══════════════════════════════════════════════════════════════
with tab_projetos:
    if len(df_f) == 0:
        st.info("Nenhum projeto encontrado.")
    else:
        # Exibição enriquecida
        df_view = df_f.copy()
        df_view["⭐"] = df_view["Classificação"].apply(estrelas)
        df_view["Progresso"] = df_view["Progresso"].apply(lambda x: f"{x}%")
 
        st.dataframe(
            df_view[["Nome","Categoria","Ano","Status","⭐","Progresso","Responsável"]],
            use_container_width=True,
            hide_index=True,
        )
 
        st.divider()
        st.markdown("### 🗑 Excluir Projeto")
        nomes = df_f["Nome"].tolist()
        nome_del = st.selectbox("Selecione o projeto para excluir", ["— selecione —"] + nomes)
        if nome_del != "— selecione —":
            if st.button(f"❌ Excluir '{nome_del}'", type="secondary"):
                st.session_state.projetos = st.session_state.projetos[
                    st.session_state.projetos["Nome"] != nome_del
                ].reset_index(drop=True)
                st.success(f"Projeto '{nome_del}' excluído.")
                st.rerun()
 
        st.divider()
        st.markdown("### 📤 Exportar CSV")
        csv_bytes = df_f.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="⬇ Baixar CSV filtrado",
            data=csv_bytes,
            file_name="pmo_projetos.csv",
            mime="text/csv",
        )
 
 
# ══════════════════════════════════════════════════════════════
# TAB 3 — ADICIONAR / EDITAR
# ══════════════════════════════════════════════════════════════
with tab_add:
    st.markdown("### ➕ Cadastrar / Editar Projeto")
 
    # Editar existente?
    df_cur = st.session_state.projetos
    modo = st.radio("Modo", ["Novo projeto", "Editar projeto existente"], horizontal=True)
 
    valores_default = {
        "Nome": "", "Categoria": CATEGORIAS_PADRAO[0], "Ano": datetime.now().year,
        "Status": "Em Andamento", "Classificação": 3, "Progresso": 0, "Responsável": ""
    }
 
    if modo == "Editar projeto existente" and len(df_cur) > 0:
        nome_edit = st.selectbox("Selecione o projeto", df_cur["Nome"].tolist())
        row = df_cur[df_cur["Nome"] == nome_edit].iloc[0]
        valores_default = row.to_dict()
 
    with st.form("form_projeto", clear_on_submit=(modo == "Novo projeto")):
        c1, c2 = st.columns(2)
        with c1:
            nome    = st.text_input("Nome do Projeto *", value=str(valores_default["Nome"]))
            cat_opts = sorted(set(CATEGORIAS_PADRAO + df_cur["Categoria"].tolist())) if len(df_cur) > 0 else CATEGORIAS_PADRAO
            cat_idx  = cat_opts.index(valores_default["Categoria"]) if valores_default["Categoria"] in cat_opts else 0
            cat     = st.selectbox("Categoria *", cat_opts, index=cat_idx)
            cat_nova = st.text_input("Ou digitar nova categoria", placeholder="Ex: Inovação")
        with c2:
            ano     = st.number_input("Ano *", min_value=2000, max_value=2099, value=int(valores_default["Ano"]))
            status_opts = list(STATUS_CORES.keys())
            st_idx  = status_opts.index(valores_default["Status"]) if valores_default["Status"] in status_opts else 0
            status  = st.selectbox("Status *", status_opts, index=st_idx)
 
        c3, c4 = st.columns(2)
        with c3:
            classif = st.slider("Classificação ⭐", 1, 5, int(valores_default["Classificação"]))
            progress = st.slider("Progresso (%)", 0, 100, int(valores_default["Progresso"]))
        with c4:
            owner   = st.text_input("Responsável", value=str(valores_default.get("Responsável","")))
 
        submitted = st.form_submit_button("💾 Salvar Projeto", type="primary", use_container_width=True)
 
        if submitted:
            if not nome.strip():
                st.error("O nome do projeto é obrigatório.")
            else:
                cat_final = cat_nova.strip() if cat_nova.strip() else cat
                novo = {
                    "Nome": nome.strip(),
                    "Categoria": cat_final,
                    "Ano": int(ano),
                    "Status": status,
                    "Classificação": classif,
                    "Progresso": progress,
                    "Responsável": owner.strip(),
                }
 
                df_cur = st.session_state.projetos
 
                if modo == "Editar projeto existente" and len(df_cur) > 0:
                    idx = df_cur.index[df_cur["Nome"] == nome_edit].tolist()
                    if idx:
                        for k, v in novo.items():
                            st.session_state.projetos.at[idx[0], k] = v
                        st.success(f"✅ Projeto '{nome}' atualizado!")
                    else:
                        st.session_state.projetos = pd.concat(
                            [st.session_state.projetos, pd.DataFrame([novo])], ignore_index=True
                        )
                        st.success(f"✅ Projeto '{nome}' cadastrado!")
                else:
                    st.session_state.projetos = pd.concat(
                        [st.session_state.projetos, pd.DataFrame([novo])], ignore_index=True
                    )
                    st.success(f"✅ Projeto '{nome}' cadastrado com sucesso!")
 
                st.rerun()
 
    st.divider()
    st.markdown("### ♻️ Resetar para dados de exemplo")
    if st.button("Resetar dados de exemplo"):
        st.session_state.projetos = pd.DataFrame(DADOS_EXEMPLO)
        st.success("Dados resetados!")
        st.rerun()
