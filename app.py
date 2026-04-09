import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Résultats des Scolaires - UCPA Aqua Stadium", 
    layout="wide", 
    page_icon="🏊",
    initial_sidebar_state="expanded"
)

# Import de la police Comfortaa globalement
st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;500;600;700&display=swap');</style>", unsafe_allow_html=True)

# --- 2. SYSTÈME DE SÉCURITÉ (MOT DE PASSE - VERSION NATIVE ET STABLE) ---
def check_password():
    """Renvoie True si le mot de passe est correct, bloque l'app sinon."""
    
    if st.session_state.get("password_correct", False):
        return True

    # CSS spécifique et temporaire pour la page de connexion (Fond Violet)
    st.markdown(
        """
        <style>
        /* Fond violet foncé */
        .stApp {
            background-color: #302675;
        }
        
        /* Cacher les éléments inutiles de Streamlit */
        .stDeployButton, footer, header, [data-testid="stDecoration"] {
            display: none !important;
        }

        /* Style du titre central */
        .login-title {
            color: #00a896;
            font-family: 'Comfortaa', sans-serif;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-top: 15vh;
            margin-bottom: 5px;
        }
        .login-subtitle {
            color: white;
            font-family: 'Comfortaa', sans-serif;
            font-size: 1.2rem;
            text-align: center;
            margin-bottom: 60px;
            opacity: 0.8;
        }

        /* Personnalisation native du champ Streamlit */
        div[data-testid="stTextInput"] input {
            background-color: white;
            border: 2px solid #00a896;
            border-radius: 10px;
            padding: 12px 20px;
            color: #302675;
            font-family: 'Comfortaa', sans-serif;
            font-size: 1rem;
        }
        
        div[data-testid="stTextInput"] input:focus {
            border-color: #6f42c1;
            box-shadow: 0 0 0 1px #6f42c1;
        }

        /* Personnalisation native du bouton Streamlit */
        div[data-testid="stButton"] button {
            background-color: #00a896;
            color: white;
            border: none;
            border-radius: 30px;
            padding: 10px 0px;
            font-family: 'Comfortaa', sans-serif;
            font-size: 1.1rem;
            font-weight: bold;
            transition: all 0.3s ease;
            margin-top: 20px;
        }
        div[data-testid="stButton"] button:hover {
            background-color: #008f81;
            color: white;
            transform: translateY(-2px);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Affichage du texte
    st.markdown('<div class="login-title">RÉSULTATS DES SCOLAIRES</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">de l\'UCPA AQUA STADIUM</div>', unsafe_allow_html=True)

    # Utilisation des colonnes Streamlit pour créer un formulaire centré
    col_gauche, col_centre, col_droite = st.columns([1, 1.5, 1])
    with col_centre:
        st.markdown("<p style='color: white; font-family: Comfortaa; margin-bottom: 5px; font-size: 0.9rem;'>Accès sécurisé</p>", unsafe_allow_html=True)
        
        pwd = st.text_input("Mot de passe", type="password", label_visibility="collapsed", placeholder="Saisissez votre mot de passe...")
        
        if st.button("ENTRER", use_container_width=True):
            if pwd == "Aqua2025":  # 👇 Le mot de passe est ici
                st.session_state["password_correct"] = True
                st.rerun() # Recharge la page en autorisant l'accès
            else:
                st.error("Mot de passe incorrect.")

    return False

# Blocage de l'application tant que le mot de passe n'est pas bon
if not check_password():
    st.stop()


# ==========================================
# --- LA SUITE NE S'AFFICHE QU'APRÈS CONNEXION ---
# ==========================================

# CSS DU DASHBOARD (Écrase le fond violet pour remettre le fond blanc)
st.markdown(
    """
    <style>
    :root {
        --color-bg-sidebar: #f8f9fa;
        --color-text-primary: #4b4b96; 
        --color-teal-primary: #00a896;
        --color-teal-light: #4db6ac;
        --color-blue-title: #005b96;
        --color-purple-label: #6f42c1;
        --color-grey-light: #e9ecef;
    }
    
    /* Retour au fond blanc normal */
    .stApp { background-color: #ffffff !important; }

    /* --- NETTOYAGE --- */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    header {background-color: transparent !important;}
    [data-testid="stSidebarCollapsedControl"] {
        display: block !important;
        visibility: visible !important;
        color: #4b4b96 !important; 
    }
     
    /* --- TYPOGRAPHIE --- */
    h1, h2, h3, h4, h5, h6, p, label, button, input, textarea, select, .stTooltip, .stMarkdown {
        font-family: 'Comfortaa', sans-serif !important;
        color: var(--color-text-primary) !important;
    }
     
    .stCheckbox p, .stRadio p, .stMultiSelect span, .stMultiSelect p {
        font-family: 'Comfortaa', sans-serif !important;
        font-size: 0.80rem !important;
    }
    div[data-testid="stCheckbox"] {
        min-height: 0px !important;
        margin-top: -4px !important; 
        margin-bottom: -4px !important; 
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
        font-weight: 700;
        font-size: 1rem;
        color: var(--color-purple-label) !important;
    }

    /* --- TITRES & KPIS --- */
    .title-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        padding-left: 20px;
        padding-top: 20px;
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
    }
    [data-testid="stMetricValue"] {
        color: var(--color-teal-primary) !important;
        font-weight: 700;
        font-size: 2.2rem !important;
    }
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

# --- 3. CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVNoxMgIGXdekwj5718tcBauk4vr2wm7J05_Opx5zT432nBuEol53W_HEsLe1WM8icSrK79pF3stRq/pub?gid=0&single=true&output=csv"
    try:
        df = pd.read_csv(url, on_bad_lines='skip', engine='python')
        cols = list(df.columns)
        
        # NOUVEAUX INDEX BASÉS SUR LA NOUVELLE CAPTURE D'ÉCRAN
        if len(cols) > 9:
            cols[0] = "Année scolaire"
            cols[2] = "Circonscription" 
            cols[4] = "Ecole"           
            cols[5] = "Classe"          
            cols[6] = "Diplome"         # Ancien 21, maintenant 6
            cols[7] = "Note Début"      # Ancien 26, maintenant 7
            cols[9] = "Note Fin"        # Ancien 28, maintenant 9
            
        df.columns = cols
        df = df.loc[:, ~df.columns.duplicated()]
        
        cols_to_clean = ["Année scolaire", "Circonscription", "Ecole", "Classe"]
        for c in cols_to_clean:
            if c in df.columns:
                df[c] = df[c].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erreur de lecture du fichier : {e}")
        return pd.DataFrame()

df_raw = load_data()

if not df_raw.empty:
    # --- 4. PRÉPARATION ---
    df = df_raw.copy()
    c_deb, c_fin = "Note Début", "Note Fin"
    if c_deb in df.columns and c_fin in df.columns:
        df[c_deb] = pd.to_numeric(df[c_deb], errors='coerce')
        df[c_fin] = pd.to_numeric(df[c_fin], errors='coerce')

    if "Année scolaire" in df.columns:
        def format_saison(valeur):
            val_str = str(valeur).strip().lower()
            
            # Filtre Anti-NaN Radical
            if val_str in ['nan', 'none', 'nul', '', '<na>']:
                return "Invalide"
                
            try:
                annee = int(float(valeur))
                return f"{annee}-{annee + 1}"
            except:
                return str(valeur)
                
        df["Saison"] = df["Année scolaire"].apply(format_saison)
        df = df[df["Saison"] != "Invalide"]
    else:
        df["Saison"] = "Inconnue"

    # --- 5. FILTRES ---
    st.sidebar.header("Filtres")

    def get_unique_sorted(series):
        raw_vals = series.dropna().unique()
        clean_vals = []
        for val in raw_vals:
            val_str = str(val).strip()
            if val_str.lower() not in ['nan', 'none', 'nul', '', '<na>', 'invalide']:
                clean_vals.append(val_str)
        return sorted(list(set(clean_vals)))

    choix_annees = []
    if "Saison" in df.columns:
        st.sidebar.subheader("Année Scolaire")
        annees_propres = [str(a).strip() for a in df["Saison"].unique() if str(a).strip().lower() not in ['nan', 'none', 'nul', '', '<na>']]
        annees_dispo = sorted(list(set(annees_propres)), reverse=True)
        
        for i, annee in enumerate(annees_dispo):
            if st.sidebar.checkbox(annee, value=(i==0), key=f"chk_annee_{i}"):
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
                    if st.checkbox(circo, key=f"chk_circo_{i}"): choix_circo.append(circo)
        if choix_circo: df = df[df["Circonscription"].isin(choix_circo)]

    if "Ecole" in df.columns:
        ecoles_dispo = get_unique_sorted(df["Ecole"])
        choix_ecole = []
        with st.sidebar.expander("Écoles", expanded=False):
            for i, ecole in enumerate(ecoles_dispo):
                if st.checkbox(ecole, key=f"chk_ecole_{i}"): choix_ecole.append(ecole)
        if choix_ecole: df = df[df["Ecole"].isin(choix_ecole)]

    if "Classe" in df.columns:
        classes_dispo_brutes = get_unique_sorted(df["Classe"])
        ordre_classes = ["MS", "GS", "CP", "CE1", "CE2", "CM1", "CM2"]
        def cle_de_tri(val): return ordre_classes.index(val) if val in ordre_classes else 99
        classes_dispo = sorted(classes_dispo_brutes, key=lambda x: (cle_de_tri(x), x))
        choix_classe = []
        with st.sidebar.expander("Classes", expanded=False):
            for i, classe in enumerate(classes_dispo):
                if st.checkbox(classe, key=f"chk_classe_{i}"): choix_classe.append(classe)
        if choix_classe: df = df[df["Classe"].isin(choix_classe)]

    # --- 6. DASHBOARD ---

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
    if "Classe" in df.columns:
        nb_eleves = df["Classe"].replace(['nan', 'None', ''], pd.NA).dropna().count()
    else: nb_eleves = 0

    if "Diplome" in df.columns:
        liste_valides = ["ASNS", "Pass Nautique", "Pass Nautique avec brassards"]
        nb_diplomes = df[df["Diplome"].isin(liste_valides)].shape[0]
    else: nb_diplomes = 0

    col1.metric("Nombre d'Élèves", nb_eleves)
    col2.metric("Écoles concernées", df["Ecole"].nunique() if "Ecole" in df.columns else 0)
    col3.metric("Diplômes Délivrés", nb_diplomes)
    st.markdown("---")

    config_download = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso2d', 'autoScale2d'],
        'toImageButtonOptions': {'format': 'png', 'filename': 'graphique_ucpa', 'height': 800, 'width': 1200, 'scale': 2}
    }

    def style_graph_standard(fig, height=None):
        fig.update_layout(
            font_family="Comfortaa", 
            font_color="#4b4b96", title_text=" ",
            hoverlabel=dict(font=dict(family="Comfortaa"), bgcolor="white", bordercolor="#e9ecef"),
            margin=dict(l=20, r=20, t=30, b=20), hovermode="closest",
            plot_bgcolor='white', paper_bgcolor='white',
        )
        fig.update_yaxes(showgrid=True, gridcolor='#f5f5f5', zeroline=False)
        fig.update_xaxes(showgrid=False, zeroline=False)
        if height: fig.update_layout(height=height)
        return fig

    def style_gauge(fig, height=None):
        fig.update_layout(
            font_family="Comfortaa", font_color="#4b4b96",
            margin=dict(l=25, r=25, t=30, b=10),
            plot_bgcolor='white', paper_bgcolor='white',
        )
        if height: fig.update_layout(height=height)
        return fig

    m_deb, m_fin = None, None
    if c_deb in df.columns and c_fin in df.columns:
        m_deb = round(df[c_deb].mean(), 1)
        m_fin = round(df[c_fin].mean(), 1)

    # --- SECTION 1 ---
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("<h3 style='text-align: center;'>Répartition des Diplômes</h3>", unsafe_allow_html=True)
        if "Diplome" in df.columns:
            df_dip = df.dropna(subset=["Diplome"])
            if not df_dip.empty:
                color_map = {"ASNS": "#6d9eeb", "Pass Nautique": "#c27ba0", "Aucun test": "#e06666", "Pass Nautique avec brassards": "#ead1dc", "Absent": "#cccccc"}
                fig = px.pie(df_dip, names="Diplome", hole=0.4, color="Diplome", color_discrete_map=color_map)
                fig.update_traces(textposition='inside', textinfo='value+percent', textfont=dict(color='#4b4b96'))
                st.plotly_chart(style_graph_standard(fig, 350), use_container_width=True, config=config_download)

    with g2:
        st.markdown("<h3 style='text-align: center;'>Répartition par Classe</h3>", unsafe_allow_html=True)
        if "Classe" in df.columns:
            df_clean = df[~df["Classe"].astype(str).str.lower().isin(['nul', 'nan', 'none', ''])]
            df_cls = df_clean["Classe"].value_counts().reset_index()
            df_cls.columns = ["Classe", "Nombre"]
            df_cls["order"] = df_cls["Classe"].apply(cle_de_tri)
            fig = px.bar(df_cls.sort_values("order"), x="Classe", y="Nombre", text_auto=True, color="Classe", color_discrete_sequence=px.colors.qualitative.Prism)
            fig.update_layout(showlegend=False)
            st.plotly_chart(style_graph_standard(fig, 350), use_container_width=True, config=config_download)

    st.markdown("---")

    # --- SECTION 2 ---
    c_pap, c_cls = st.columns(2)
    with c_pap:
        st.markdown("<h3 style='text-align: center;'>Glissement des Notes</h3>", unsafe_allow_html=True)
        if c_deb in df.columns and c_fin in df.columns:
            d_cnt = df[c_deb].value_counts().reindex(range(13), fill_value=0)
            f_cnt = df[c_fin].value_counts().reindex(range(13), fill_value=0)
            offset = max(d_cnt.max(), f_cnt.max()) * 0.1 
            fig = go.Figure()
            fig.add_trace(go.Bar(y=d_cnt.index, x=d_cnt.values*-1, base=-offset, name='Début', orientation='h', marker_color='#adb5bd', text=d_cnt.values, textposition='auto'))
            fig.add_trace(go.Bar(y=f_cnt.index, x=f_cnt.values, base=offset, name='Fin', orientation='h', marker_color='#00a896', text=f_cnt.values, textposition='auto'))
            fig.add_trace(go.Scatter(x=[0]*13, y=list(range(13)), mode='text', text=list(range(13)), textfont=dict(color='#4b4b96', size=13, family="Comfortaa", weight="bold"), hoverinfo='skip'))
            fig.update_layout(barmode='overlay', bargap=0.1, xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False, dtick=1), legend=dict(orientation="h", y=1.1))
            st.plotly_chart(style_graph_standard(fig, 400), use_container_width=True, config=config_download)

    with c_cls:
        st.markdown("<h3 style='text-align: center;'>Moyenne Globale</h3>", unsafe_allow_html=True)
        if pd.notna(m_deb) and pd.notna(m_fin):
            cj1, cj2 = st.columns(2)
            steps = [{'range': [0, 4], 'color': "#bf9000"}, {'range': [4, 8], 'color': "#e1ddd7"}, {'range': [8, 12], 'color': "#f5dc1e"}, {'range': [12, 13], 'color': "#9fc5e8"}]
            with cj1:
                fig_s = go.Figure(go.Indicator(mode="gauge+number", value=m_deb, title={'text': "Début", 'font': {'size': 14}}, gauge={'axis': {'range': [None, 12.2], 'tickvals': [0, 4, 8, 12]}, 'bar': {'color': "#4b4b96"}, 'steps': steps}))
                st.plotly_chart(style_gauge(fig_s, 220), use_container_width=True, config=config_download)
            with cj2:
                fig_e = go.Figure(go.Indicator(mode="gauge+number+delta", value=m_fin, title={'text': "Fin", 'font': {'size': 14}}, delta={'reference': m_deb, 'increasing': {'color': "#00a896"}}, gauge={'axis': {'range': [None, 12.2], 'tickvals': [0, 4, 8, 12]}, 'bar': {'color': "#4b4b96"}, 'steps': steps}))
                st.plotly_chart(style_gauge(fig_e, 220), use_container_width=True, config=config_download)

    st.markdown("---")

    # --- SECTION 3 : SCATTER PLOT ---
    st.markdown("<h3 style='text-align: center;'>Performance par École</h3>", unsafe_allow_html=True)
    if "Ecole" in df.columns and c_deb in df.columns and c_fin in df.columns:
        df_eco = df.groupby("Ecole").agg({c_deb: 'mean', c_fin: 'mean', df.columns[0]: 'count'}).reset_index()
        df_eco.columns = ["Ecole", "Moy_Deb", "Moy_Fin", "Nb_Eleves"]
        df_eco["Progression"] = (df_eco["Moy_Fin"] - df_eco["Moy_Deb"]).round(1)
        fig = px.scatter(df_eco, x="Moy_Deb", y="Moy_Fin", size="Nb_Eleves", color="Ecole", text="Ecole", hover_name="Ecole", color_discrete_sequence=px.colors.qualitative.Vivid, custom_data=["Moy_Deb", "Moy_Fin", "Progression", "Nb_Eleves"])
        fig.update_layout(xaxis_title="Moyenne Début", yaxis_title="Moyenne Fin", showlegend=False)
        fig.update_traces(textposition='top center')
        st.plotly_chart(style_graph_standard(fig, 550), use_container_width=True, config=config_download)

    # --- SECTION 4 : ANALYSES CLASSE & ANNÉE ---
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: #00a896;'>Analyses Comparatives : Classe & Année</h3>", unsafe_allow_html=True)
    st.markdown("") 

    if "Classe" in df.columns and "Saison" in df.columns and c_deb in df.columns and c_fin in df.columns:
        
        # Calcul de la moyenne ET du compte des élèves
        df_valid_classes = df[~df["Classe"].astype(str).str.lower().isin(['nul', 'nan', 'none', ''])]
        
        df_group = df_valid_classes.groupby(["Classe", "Saison"]).agg(
            Moy_Deb=(c_deb, 'mean'),
            Nb_Deb=(c_deb, 'count'),
            Moy_Fin=(c_fin, 'mean'),
            Nb_Fin=(c_fin, 'count')
        ).reset_index()
        
        # On remet les noms originaux pour la compatibilité avec Plotly
        df_group[c_deb] = df_group["Moy_Deb"].round(1)
        df_group[c_fin] = df_group["Moy_Fin"].round(1)

        df_group["order"] = df_group["Classe"].apply(cle_de_tri)
        df_group = df_group.sort_values(["order", "Saison"])
        saisons_triees = sorted(df_group["Saison"].unique())
         
        ca1, ca2 = st.columns(2)
        with ca1:
            st.markdown("<h4 style='text-align: center;'>Niveau Début</h4>", unsafe_allow_html=True)
            
            fig_deb = px.bar(
                df_group, x="Classe", y=c_deb, color="Saison", barmode="group", text_auto='.1f', 
                color_discrete_sequence=px.colors.qualitative.Pastel, category_orders={"Saison": saisons_triees},
                custom_data=["Nb_Deb"] 
            )
            fig_deb.update_traces(
                textangle=0, textposition='outside', 
                hovertemplate="<b>%{x}</b><br>Année : %{fullData.name}<br>Note : %{y:.1f}<br>Nombre d'élèves : %{customdata[0]}<extra></extra>"
            )
            fig_deb.update_layout(yaxis_title="Note Moyenne", yaxis_range=[0, 13])
            st.plotly_chart(style_graph_standard(fig_deb, 500), use_container_width=True, config=config_download)
             
        with ca2:
            st.markdown("<h4 style='text-align: center;'>Niveau Fin</h4>", unsafe_allow_html=True)
            
            fig_fin = px.bar(
                df_group, x="Classe", y=c_fin, color="Saison", barmode="group", text_auto='.1f', 
                color_discrete_sequence=px.colors.qualitative.Pastel, category_orders={"Saison": saisons_triees},
                custom_data=["Nb_Fin"] 
            )
            fig_fin.update_traces(
                textangle=0, textposition='outside', 
                hovertemplate="<b>%{x}</b><br>Année : %{fullData.name}<br>Note : %{y:.1f}<br>Nombre d'élèves : %{customdata[0]}<extra></extra>"
            )
            fig_fin.update_layout(yaxis_title="Note Moyenne", yaxis_range=[0, 13])
            st.plotly_chart(style_graph_standard(fig_fin, 500), use_container_width=True, config=config_download)
    else: st.info("Données insuffisantes pour l'analyse par année.")

    # --- PIED DE PAGE ---
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #4b4b96; font-family: \"Comfortaa\"; font-size: 0.8rem; opacity: 0.8;'>© 2026 UCPA Aqua Stadium</div>", unsafe_allow_html=True)

else: st.info("Chargement des données en cours...")
