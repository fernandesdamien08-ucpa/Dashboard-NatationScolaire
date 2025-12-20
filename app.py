import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Dashboard Natation", layout="wide", page_icon="🏊")

# --- 2. CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    # 👇 COLLE TON LIEN GOOGLE SHEETS ENTRE LES GUILLEMETS ICI 👇
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQEtHKsiIf4zjKsdYoW9TAFFTLaiXGw9rQwdNRV0nexX179GYktIeqWfMFv0IRV0Col0quuyGc6DSqG/pub?output=csv"
    
    try:
        df = pd.read_csv(url)
        # Nettoyage optionnel : on force certains formats si besoin
        # df['Année scolaire'] = df['Année scolaire'].astype(str) 
        return df
    except Exception as e:
        st.error(f"Erreur de lecture du CSV. Vérifie le lien. Détail : {e}")
        return pd.DataFrame() # Retourne vide en cas d'erreur

df = load_data()

# Si le fichier est chargé, on lance l'app
if not df.empty:

    # --- 3. BARRE LATÉRALE (FILTRES) ---
    st.sidebar.header("🔍 Filtres")

    # Filtre Année (Sélecteur unique pour ne pas mélanger les années)
    # Vérification si la colonne existe pour éviter les erreurs
    if "Année scolaire" in df.columns:
        annees = df["Année scolaire"].unique()
        choix_annee = st.sidebar.selectbox("Année Scolaire", sorted(annees, reverse=True))
        df = df[df["Année scolaire"] == choix_annee]

    # Filtre Circonscription
    if "Circonscription" in df.columns:
        circo_dispo = df["Circonscription"].unique()
        choix_circo = st.sidebar.multiselect("Circonscription", circo_dispo, default=circo_dispo)
        # On filtre si l'utilisateur a sélectionné quelque chose
        if choix_circo:
            df = df[df["Circonscription"].isin(choix_circo)]

    # Filtre École
    if "Ecole" in df.columns:
        ecoles_dispo = df["Ecole"].unique()
        choix_ecole = st.sidebar.multiselect("École", ecoles_dispo)
        if choix_ecole:
            df = df[df["Ecole"].isin(choix_ecole)]

    # --- 4. CORPS DU TABLEAU DE BORD ---
    st.title(f"🏊 Suivi Natation Scolaire - {choix_annee if 'Année scolaire' in df.columns else ''}")
    st.markdown("---")

    # --- LIGNE 1 : KPIs (Chiffres clés) ---
    col1, col2, col3, col4 = st.columns(4)

    nb_eleves = len(df)
    nb_classes = df["Classe"].nunique() if "Classe" in df.columns else 0
    nb_ecoles = df["Ecole"].nunique() if "Ecole" in df.columns else 0
    # Exemple de calcul : Taux de réussite (Si 'Diplome' contient 'OUI' ou un niveau validé)
    # Tu pourras adapter cette logique selon ce qu'il y a dans ta colonne "Diplome"
    nb_diplomes = df["Diplome"].count() if "Diplome" in df.columns else 0

    col1.metric("Nombre d'Élèves", nb_eleves)
    col2.metric("Classes Concernées", nb_classes)
    col3.metric("Écoles", nb_ecoles)
    col4.metric("Diplômes/Niveaux actés", nb_diplomes)

    st.markdown("---")

    # --- LIGNE 2 : GRAPHIQUES ---
    g1, g2 = st.columns(2)

    with g1:
        st.subheader("📊 Répartition par Niveau (Fin de cycle)")
        if "Niveau fin de cycle" in df.columns:
            # Graphique camembert
            fig_pie = px.pie(df, names="Niveau fin de cycle", title="Niveaux validés")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("Colonne 'Niveau fin de cycle' introuvable.")

    with g2:
        st.subheader("🏫 Élèves par Circonscription")
        if "Circonscription" in df.columns:
            # Graphique barres
            df_circo = df["Circonscription"].value_counts().reset_index()
            df_circo.columns = ["Circonscription", "Nombre"]
            fig_bar = px.bar(df_circo, x="Circonscription", y="Nombre", color="Circonscription")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Colonne 'Circonscription' introuvable.")

    # --- LIGNE 3 : ANALYSE DÉTAILLÉE ---
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Élèves par MNS (Encadrants)")
        if "MNS" in df.columns:
            df_mns = df.groupby("MNS").size().reset_index(name='Nombre d\'élèves')
            fig_mns = px.bar(df_mns, x="MNS", y="Nombre d\'élèves", text_auto=True)
            st.plotly_chart(fig_mns, use_container_width=True)

    with c2:
        st.subheader("Données brutes filtrées")
        st.dataframe(df, use_container_width=True)

else:
    st.info("En attente du chargement des données...")