import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Résultats des Scolaires - UCPA Aqua Stadium", layout="wide", page_icon="🏊")

# --- CSS PERSONNALISÉ ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;500;600;700&display=swap');

    :root {
        --color-bg-main: #ffffff;
        --color-bg-sidebar: #f8f9fa;
        --color-text-primary: #4b4b96; 
        --color-teal-primary: #00a896;
        --color-teal-light: #4db6ac;
        --color-blue-title: #005b96;
        --color-purple-label: #6f42c1;
        --color-grey-light: #e9ecef;
    }

    /* --- POLICE GLOBALE --- */
    h1, h2, h3, h4, h5, h6, p, label, button, input, textarea, select, .stTooltip, .stMarkdown {
        font-family: 'Comfortaa', sans-serif !important;
        color: var(--color-text-primary) !important;
    }
    
    /* --- TAILLE POLICE CHECKBOX --- */
    .stCheckbox p, .stRadio p, .stMultiSelect span, .stMultiSelect p {
        font-family: 'Comfortaa', sans-serif !important;
        font-size: 0.85rem !important;
        color: var(--color-text-primary) !important;
    }

    /* --- 1. RÉGLAGE ESPACEMENT LISTES SIMPLES --- */
    div[data-testid="stCheckbox"] {
        min-height: 0px !important;
        margin-top: -4px !important; 
        margin-bottom: -4px !important; 
    }

    /* --- 2. RÉGLAGE SPÉCIAL CIRCONSCRIPTIONS --- */
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        min-height: 0px !important;
        padding: 0px !important;
        margin-top: -8px !important;
        margin-bottom: -8px !important;
        align-items: center !important;
    }

    [data-testid="stSidebar"] [data-testid="stImage"] {
        margin-bottom: 0px !important;
        margin-top: 0px !important;
    }
    
    [data-testid="stSidebar"] [data-testid="column"] {
        display: flex !important;
        align-items: center !important;
    }

    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] {
        background-color: var(--color-bg-sidebar);
        border-right: 1px solid var(--color-grey-light);
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background-color: white;
        border-radius: 8px;
        border: 1px solid var(--color-grey-light);
        margin-bottom: 5px;
        color: var(--color-purple-label);
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader p {
        font-family: 'Comfortaa', sans-serif !important;
        font-weight: 700;
        font-size: 1rem;
        color: var(--color-purple-label) !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader svg, 
    [data-testid="stSidebar"] .streamlit-expanderHeader i {
        font-family: inherit !important;
    }

    /* --- TITRES --- */
    .title-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        padding-left: 20px;
    }
    
    .main-title-1 {
        color: var(--color-teal-primary) !important;
        font-family: 'Comfortaa', sans-serif !important;
        font-weight: 400;
        font-size: 2.2rem;
        text-transform: uppercase;
        line-height: 1.1;
        margin-bottom: 5px;
    }
    
    .main-title-2 {
        color: #4b4b96 !important;
        font-family: 'Comfortaa', sans-serif !important;
        font-weight: 300;
        font-size: 1.5rem;
        line-height: 1.1;
    }

    /* --- KPIS --- */
    [data-testid="stMetric"] {
        background-color: white;
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid var(--color-grey-light);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    [data-testid="stMetricLabel"] {
        color: var(--color-purple-label) !important;
        font-weight: 700;
        text-transform: uppercase;
        font-family: 'Comfortaa', sans-serif !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--color-teal-primary) !important;
        font-weight: 700;
        font-size: 2.2rem !important;
    }
    
    /* --- GRAPHIQUES "CLEAN LOOK" --- */
    [data-testid="stPlotlyChart"] {
        background-color: white;
        padding: 0px;
        border-radius: 0px;
        border: none;
        box-shadow: none;
    }
    
    hr {
        margin: 1.5rem 0;
        border-color: var(--color-teal-light);
        opacity: 0.3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQEtHKsiIf4zjKsdYoW9TAFFTLaiXGw9rQwdNRV0nexX179GYktIeqWfMFv0IRV0Col0quuyGc6DSqG/pub?output=csv"
    try:
        df = pd.read_csv(url, on_bad_lines='skip', engine='python')
        df.columns = df.columns.str.strip()
        cols_text = ["Année scolaire", "Circonscription", "Ecole", "Classe"]
        for c in cols_text:
            if c in df.columns:
                df[c] = df[c].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erreur CSV : {e}")
        return pd.DataFrame()

df_raw = load_data()

if not df_raw.empty:

    # --- 3. PRÉPARATION ---
    if "Année scolaire" in df_raw.columns:
        df = df_raw.copy()
        df = df[df["Année scolaire"] != 'nan']
        
        def format_saison(valeur):
            try:
                annee = int(float(valeur))
                return f"{annee}-{annee + 1}"
            except:
                return str(valeur)
        df["Saison"] = df["Année scolaire"].apply(format_saison)
    else:
        df = df_raw.copy()
        df["Saison"] = "Inconnue"

    # --- 4. FILTRES ---
    st.sidebar.header("Filtres")

    def get_unique_sorted(series):
        return sorted(list(set(series.dropna().unique())), reverse=False)

    choix_annees = []
    if "Saison" in df.columns:
        st.sidebar.subheader("Année Scolaire")
        annees_dispo = sorted(list(set(df["Saison"].unique())), reverse=True)
        for i, annee in enumerate(annees_dispo):
            if st.sidebar.checkbox(annee, value=(i==0), key=f"chk_annee_{i}_v39"):
                choix_annees.append(annee)
        if choix_annees: df = df[df["Saison"].isin(choix_annees)]

    st.sidebar.markdown("---")

    if "Circonscription" in df.columns:
        circo_dispo = get_unique_sorted(df["Circonscription"])
        choix_circo = []
        logos_villes = {
            "mérignac": "https://media.licdn.com/dms/image/v2/C4D0BAQHH-t_ZsrR0oQ/company-logo_200_200/company-logo_200_200/0/1631330164292?e=2147483647&v=beta&t=yRIRvQPqQGDJRQeCquZpVT0UZ12pLrdJtV4n3z3GM5A",
            "martignas": "https://www.pagesjaunes.fr/media/agc/68/2f/30/00/00/36/00/04/50/f0/6622682f30000036000450f0/662268313000005a700450f3.png",
            "bordeaux": "https://upload.wikimedia.org/wikipedia/fr/thumb/5/5f/Ville_de_Bordeaux_%28logo%29.svg/1015px-Ville_de_Bordeaux_%28logo%29.svg.png"
        }
        with st.sidebar.expander("Circonscriptions", expanded=False):
            for i, circo in enumerate(circo_dispo):
                col_img, col_chk = st.columns([0.15, 0.85])
                logo = None
                if "mérignac" in str(circo).lower(): logo = logos_villes["mérignac"]
                elif "martignas" in str(circo).lower(): logo = logos_villes["martignas"]
                elif "bordeaux" in str(circo).lower(): logo = logos_villes["bordeaux"]
                
                with col_img:
                    if logo: st.image(logo, width=25)
                    else: st.write("")
                with col_chk:
                    if st.checkbox(circo, key=f"chk_circo_{i}_v39"): choix_circo.append(circo)
        if choix_circo: df = df[df["Circonscription"].isin(choix_circo)]

    if "Ecole" in df.columns:
        ecoles_dispo = get_unique_sorted(df["Ecole"])
        choix_ecole = []
        with st.sidebar.expander("Écoles", expanded=False):
            for i, ecole in enumerate(ecoles_dispo):
                if st.checkbox(ecole, key=f"chk_ecole_{i}_v39"): choix_ecole.append(ecole)
        if choix_ecole: df = df[df["Ecole"].isin(choix_ecole)]

    if "Classe" in df.columns:
        classes_brutes = get_unique_sorted(df["Classe"])
        classes_propres = [c for c in classes_brutes if str(c).lower() not in ['nul', 'nan', 'none', '']]
        ordre_classes = ["MS", "GS", "CP", "CE1", "CE2", "CM1", "CM2"]
        def cle_de_tri(val): return ordre_classes.index(val) if val in ordre_classes else 99
        classes_dispo = sorted(classes_propres, key=lambda x: (cle_de_tri(x), x))
        choix_classe = []
        with st.sidebar.expander("Classes", expanded=False):
            for i, classe in enumerate(classes_dispo):
                if st.checkbox(classe, key=f"chk_classe_{i}_v39"): choix_classe.append(classe)
        if choix_classe: df = df[df["Classe"].isin(choix_classe)]

    # --- 5. DASHBOARD ---

    col_logo, col_titre = st.columns([1, 4])
    with col_logo:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbnl2xYxkNEnecCkFnY7lVGZ1DyF1K3JQvQA&s", width=200)
    with col_titre:
        st.markdown(
            """
            <div class="title-container">
                <div class="main-title-1">RÉSULTATS DES SCOLAIRES</div>
                <div class="main-title-2">de l'UCPA AQUA STADIUM</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    if "Prénom" in df.columns: nb_eleves = df["Prénom"].notna().sum()
    elif "Prenom" in df.columns: nb_eleves = df["Prenom"].notna().sum()
    else: nb_eleves = len(df)

    if "Diplome" in df.columns:
        liste_valides = ["ASNS", "Pass Nautique", "Pass Nautique avec brassards"]
        nb_diplomes = df[df["Diplome"].isin(liste_valides)].shape[0]
    else: nb_diplomes = 0

    col1.metric("Nombre d'Élèves", nb_eleves)
    col2.metric("Écoles concernées", df["Ecole"].nunique() if "Ecole" in df.columns else 0)
    col3.metric("Diplômes Délivrés", nb_diplomes)
    st.markdown("---")

    # --- CONFIGURATION DU TÉLÉCHARGEMENT IMAGE (HD) ---
    config_download = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso2d', 'autoScale2d'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'graphique_ucpa',
            'height': 800,
            'width': 1200,
            'scale': 2
        }
    }

    # --- STYLES GRAPHIQUES ---
    def style_graph_standard(fig, height=None):
        fig.update_layout(
            font_family="Comfortaa", 
            font_color="#4b4b96", 
            title=None,
            hoverlabel=dict(font=dict(family="Comfortaa"), bgcolor="white", bordercolor="#e9ecef"),
            margin=dict(l=20, r=20, t=30, b=20), hovermode="closest",
            title_text="",
            legend=dict(font=dict(color="#4b4b96")),
            plot_bgcolor='white',
            paper_bgcolor='white',
        )
        fig.update_yaxes(showgrid=True, gridcolor='#f5f5f5', zeroline=False)
        fig.update_xaxes(showgrid=False, zeroline=False)
        
        if height: fig.update_layout(height=height)
        return fig

    def style_gauge(fig, height=None):
        fig.update_layout(
            font_family="Comfortaa", 
            font_color="#4b4b96",
            title=None,
            margin=dict(l=25, r=25, t=30, b=10),
            title_text="",
            plot_bgcolor='white',
            paper_bgcolor='white',
        )
        if height: fig.update_layout(height=height)
        return fig

    # --- CALCULS GLOBAUX ---
    c_deb, c_fin, m_deb, m_fin = None, None, None, None
    if len(df.columns) > 30:
        c_deb, c_fin = df.columns[28], df.columns[30]
        m_deb = round(pd.to_numeric(df[c_deb], errors='coerce').mean(), 1)
        m_fin = round(pd.to_numeric(df[c_fin], errors='coerce').mean(), 1)

    # --- SECTION 1 ---
    g1, g2 = st.columns(2)

    with g1:
        st.markdown("<h3 style='text-align: center;'>Répartition des Diplômes</h3>", unsafe_allow_html=True)
        if "Diplome" in df.columns:
            df_dip = df.dropna(subset=["Diplome"])
            if not df_dip.empty:
                color_map = {"ASNS": "#6d9eeb", "Pass Nautique": "#c27ba0", "Aucun test": "#e06666", 
                             "Pass Nautique avec brassards": "#ead1dc", "Absent": "#cccccc"}
                fig = px.pie(df_dip, names="Diplome", hole=0.4, color="Diplome", color_discrete_map=color_map)
                
                # --- INFOBULLE PERSONNALISÉE ---
                fig.update_traces(
                    textposition='inside', 
                    textinfo='value+percent', 
                    hovertemplate = "<b>%{label}</b><br>Nombre : %{value}<br>Part : %{percent}<extra></extra>", # <-- C'est ici !
                    textfont=dict(color='#4b4b96')
                )
                
                fig = style_graph_standard(fig, height=350)
                st.plotly_chart(fig, use_container_width=True, config=config_download)
            else: st.info("Pas de données.")

    with g2:
        st.markdown("<h3 style='text-align: center;'>Répartition par Classe</h3>", unsafe_allow_html=True)
        if "Classe" in df.columns:
            df_clean = df[~df["Classe"].astype(str).str.lower().isin(['nul', 'nan', 'none', ''])]
            df_cls = df_clean["Classe"].value_counts().reset_index()
            df_cls.columns = ["Classe", "Nombre"]
            df_cls["order"] = df_cls["Classe"].apply(cle_de_tri)
            df_cls = df_cls.sort_values("order")
            
            fig = px.bar(df_cls, x="Classe", y="Nombre", text_auto=True, color="Classe", 
                         color_discrete_sequence=px.colors.qualitative.Prism)
            fig.update_layout(showlegend=False)
            fig = style_graph_standard(fig, height=350)
            st.plotly_chart(fig, use_container_width=True, config=config_download)

    st.markdown("---")

    # --- SECTION 2 ---
    c_pap, c_cls = st.columns(2)

    with c_pap:
        st.markdown("<h3 style='text-align: center;'>Glissement des Notes</h3>", unsafe_allow_html=True)
        if len(df.columns) > 30:
            d_cnt = df[c_deb].value_counts().reindex(range(13), fill_value=0)
            f_cnt = df[c_fin].value_counts().reindex(range(13), fill_value=0)
            
            max_val = max(d_cnt.max(), f_cnt.max())
            offset = max_val * 0.1 
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=d_cnt.index, 
                x=d_cnt.values*-1, 
                base=-offset, 
                name='Début', 
                orientation='h', 
                marker_color='#adb5bd', 
                text=d_cnt.values, 
                textposition='auto', 
                hovertemplate='<b>Début</b><br>Note: %{y}<br>Élèves: %{text}<extra></extra>'
            ))
            
            fig.add_trace(go.Bar(
                y=f_cnt.index, 
                x=f_cnt.values, 
                base=offset, 
                name='Fin', 
                orientation='h', 
                marker_color='#00a896', 
                text=f_cnt.values, 
                textposition='auto', 
                hovertemplate='<b>Fin</b><br>Note: %{y}<br>Élèves: %{text}<extra></extra>'
            ))
            
            fig.add_trace(go.Scatter(
                x=[0] * 13,
                y=list(range(13)),
                mode='text',
                text=list(range(13)),
                textfont=dict(color='#4b4b96', size=13, family="Comfortaa", weight="bold"),
                marker=dict(opacity=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.update_layout(
                barmode='overlay', 
                bargap=0.1, 
                xaxis=dict(showticklabels=False, title="Nb Élèves", showgrid=False, zeroline=False), 
                yaxis=dict(showticklabels=False, showgrid=False, title=""),
                legend=dict(orientation="h", y=1.1)
            )
            
            fig = style_graph_standard(fig, height=400)
            fig.update_yaxes(showgrid=False) 
            fig.update_xaxes(showgrid=False)
            st.plotly_chart(fig, use_container_width=True, config=config_download)

    with c_cls:
        st.markdown("<h3 style='text-align: center;'>Moyenne Globale</h3>", unsafe_allow_html=True)
        if pd.notna(m_deb) and pd.notna(m_fin):
            cj1, cj2 = st.columns(2)
            with cj1:
                fig_s = go.Figure(go.Indicator(
                    mode="gauge+number", value=m_deb, title={'text': "Début", 'font': {'size': 14, 'family': 'Comfortaa', 'color': '#4b4b96'}},
                    gauge={'axis': {'range': [None, 12], 'tickfont': {'family': 'Comfortaa', 'color': '#4b4b96'}}, 'bar': {'color': "#adb5bd"}}))
                fig_s = style_gauge(fig_s, height=220)
                st.plotly_chart(fig_s, use_container_width=True, config=config_download)
            with cj2:
                fig_e = go.Figure(go.Indicator(
                    mode="gauge+number+delta", value=m_fin, title={'text': "Fin", 'font': {'size': 14, 'family': 'Comfortaa', 'color': '#4b4b96'}},
                    delta={'reference': m_deb, 'increasing': {'color': "#00a896"}},
                    gauge={'axis': {'range': [None, 12], 'tickfont': {'family': 'Comfortaa', 'color': '#4b4b96'}}, 'bar': {'color': "#00a896"}}))
                fig_e = style_gauge(fig_e, height=220)
                st.plotly_chart(fig_e, use_container_width=True, config=config_download)
        else: st.info("Données insuffisantes.")

    st.markdown("---")

    # --- SECTION 3 : SCATTER PLOT ---
    st.markdown("<h3 style='text-align: center;'>Performance par École</h3>", unsafe_allow_html=True)
    if "Ecole" in df.columns and len(df.columns) > 30:
        df_eco = df.groupby("Ecole").agg({c_deb: 'mean', c_fin: 'mean', df.columns[0]: 'count'}).reset_index()
        df_eco.columns = ["Ecole", "Moy_Deb", "Moy_Fin", "Nb_Eleves"]
        
        df_eco["Moy_Deb"] = df_eco["Moy_Deb"].round(1)
        df_eco["Moy_Fin"] = df_eco["Moy_Fin"].round(1)
        df_eco["Progression"] = (df_eco["Moy_Fin"] - df_eco["Moy_Deb"]).round(1)
        
        x_min, x_max = df_eco["Moy_Deb"].min(), df_eco["Moy_Deb"].max()
        y_min, y_max = df_eco["Moy_Fin"].min(), df_eco["Moy_Fin"].max()
        pad = 0.5 
        
        fig = px.scatter(df_eco, x="Moy_Deb", y="Moy_Fin", size="Nb_Eleves", color="Ecole", 
                         text="Ecole", hover_name="Ecole", 
                         color_discrete_sequence=px.colors.qualitative.Vivid,
                         custom_data=["Moy_Deb", "Moy_Fin", "Progression", "Nb_Eleves"])
        
        fig.update_layout(
            xaxis_range=[x_min - pad, x_max + pad], 
            yaxis_range=[y_min - pad, y_max + pad],
            xaxis_title="Moyenne Début", yaxis_title="Moyenne Fin",
            showlegend=False,
            title_text=""
        )
        
        fig.update_traces(
            textposition='top center',
            hovertemplate="<b>%{hovertext}</b><br><br>" +
            "Début : %{customdata[0]:.1f}<br>" +
            "Fin : %{customdata[1]:.1f}<br>" +
            "Progression : %{customdata[2]:+.1f}<br>" + 
            "Élèves : %{customdata[3]}<extra></extra>"
        )
        
        fig = style_graph_standard(fig, height=550)
        fig.update_xaxes(showgrid=True, gridcolor='#f5f5f5')
        fig.update_yaxes(showgrid=True, gridcolor='#f5f5f5')
        
        st.plotly_chart(fig, use_container_width=True, config=config_download)

    # --- PIED DE PAGE ---
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #4b4b96; font-family: "Comfortaa"; padding-top: 20px; font-size: 0.8rem; opacity: 0.8;'>
            © 2025 UCPA Aqua Stadium - Document destiné aux services de la Ville et de l'Éducation Nationale
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("Chargement...")
