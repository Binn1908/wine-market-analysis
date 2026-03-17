from pathlib import Path

from PIL import Image
import streamlit as st

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"

def tab_presentation():
	st.title('Présentation')

	tab1, tab2 = st.tabs(['Contexte', 'Méthodologie/Outils'])

	with tab1:
		
		col1, col2 = st.columns(2)

		with col1:
			st.subheader("Contexte de l'analyse")
			st.write('- Lancement du produit *Domaine des Croix 2016 Corton Grèves* sur le marché américain')
			st.write("- **Objectif :** Comprendre le marché afin d'établir un prix compétitif")

			st.subheader("Base de données")
			st.write('- [130.000 références](https://github.com/WildCodeSchool/wilddata/raw/main/wine_df.zip) de bouteilles de vin distribuées aux Etats-Unis')
			st.write("- **Informations pertinentes :** cépage, région et année de production, note, descriptif d'expert, prix moyen en dollars")

		with col2:

			st.image(Image.open(ASSETS / "bouteille.jpeg"), width=450)

	with tab2:
		st.subheader('Méthodologie et outils')
		st.write('**1) Préparation des données**')
		st.markdown('- Nettoyage et filtrage des valeurs manquantes -> 120.904 vins retenus sur 130.000')

		st.write('**2) Exploration des données**')
		st.markdown(
      		'- Analyse descriptive du marché (notes, prix, cépages) avec Pandas et Matplotlib\n'
			'- Visualisation géographique des notes moyenne par pays avec Plotly\n'
			'- Analyse sémantique des descriptions d\'experts avec NLTK et WordCloud'
   		)

		st.write('**3) Synthèse**')
		st.markdown('- Mise en forme des résultats dans un tableau de bord interactif Streamlit')
