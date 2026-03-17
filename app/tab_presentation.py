import streamlit as sl
from PIL import Image

def tab_presentation():
	sl.title('Présentation')

	tab1, tab2, tab3 = sl.tabs(['Contexte', 'Méthodologie/Outils', 'Code'])

	with tab1:
		
		col1, col2 = sl.columns([1,1])

		with col1:
			sl.subheader("Contexte de l'analyse")
			sl.write('- Lancement du produit *Domaine des Croix 2016 Corton Grèves* sur le marché américain')
			sl.write("- **Objectif :** Comprendre le marché afin d'établir un prix compétitif")

			sl.subheader("Base de données")
			sl.write('- [130.000 références](https://github.com/WildCodeSchool/wilddata/raw/main/wine_df.zip) de bouteilles de vin distribuées aux Etats-Unis')
			sl.write("- **Informations pertinentes :** cépage, région et année de production, note, descriptif d'expert, prix moyen en dollars")

		with col2:
			img = Image.open('bouteille.jpeg')
			sl.image(img)

	with tab2:
		sl.subheader('Méthodologie et outils')
		sl.write('**1) Préparation des données**')
		sl.write('- Suppression des valeurs manquantes dans la base de données avec Python et Pandas')
		sl.write('- Dimension du dataset final : 120.904 lignes')

		sl.write('**2) Exploration des données**')
		sl.write('- Analyse descriptive du marché du vin avec Matplotlib')
		sl.write('- Carte chloroplèthe avec Plotly')
		sl.write('- WordCloud avec NLTK (*Natural Language Toolkit*)')

		sl.write('**3) Synthèse**')
		sl.write('- Création du tableau de bord via une application Streamlit')

	with tab3:
		sl.subheader("Code de l'analyse")

		sl.write('**NLP**')
		body = """
		import nltk
		nltk.download('popular')
		import re
		from nltk.corpus import stopwords
		from nltk.stem import SnowballStemmer

		def cleaning(text):
			text = text.lower()
			text = re.sub(r'[^\w\s]', '', text)
			tokens = nltk.word_tokenize(text)
			stopwords = nltk.corpus.stopwords.words("english")
			tokens_clean = [token for token in tokens if token not in stopwords]
			stemmer = SnowballStemmer("english")
			tokens_stemmed = [stemmer.stem(token) for token in tokens_clean]
			text_clean = " ".join(tokens_stemmed)
			return text_clean

		df['description_clean'] = df.description.apply(cleaning)

		from wordcloud import WordCloud
		import matplotlib.pyplot as plt

		wordcloud = WordCloud(width = 480, height = 480, max_font_size = 200, min_font_size = 10)
		wordcloud.generate_from_text(' '.join(df['description_clean']))
		plt.figure()
		plt.imshow(wordcloud, interpolation = 'bilinear')
		plt.axis('off')
		plt.show()
		"""
		sl.code(body, language = 'python', line_numbers = True)
