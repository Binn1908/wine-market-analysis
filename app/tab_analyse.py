import streamlit as sl
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
#from wordcloud import WordCloud
from PIL import Image

@sl.cache_data
def load_df():
	df1 = pd.read_pickle('df_clean1.pickle')
	df2 = pd.read_pickle('df_clean2.pickle')
	df3 = pd.read_pickle('df_clean3.pickle')
	df4 = pd.read_pickle('df_clean4.pickle')
	df = pd.concat([df1, df2, df3, df4])
	return df

df = load_df()

def tab_analyse():
	sl.title('Analyse')

	tab1, tab2, tab3, tab4 = sl.tabs(['Analyse exploratoire', 'Descriptions', 'Comparateur de prix', 'Conseil'])

	with tab1:
		sl.write('**Note moyenne par pays**')
		df_country = df.groupby(by = ['country', 'code'], as_index = False)['points'].mean()
		fig = px.choropleth(df_country, 
			locations = 'code', 
			color = 'points', 
			hover_name = 'country', 
			color_continuous_scale = [[0, 'rgb(255,255,255)'], [1, 'rgb(166,24,46)']])
		#projection='natural earth'
		sl.plotly_chart(fig)

		col1, col2 = sl.columns([1,1])

		with col1:
			sl.write('**Top 10 - Répartition des vins par pays**')
			labels = df.country.value_counts().nlargest(10).index
			sizes = df.country.value_counts().nlargest(10)
			fig, ax = plt.subplots()
			ax.pie(sizes, labels = labels, autopct = '%1.1f%%')
			sl.pyplot(fig)

		with col2:
			sl.write('**Top 10 - Les pays les mieux notés**')
			y = df.groupby(by = 'country')['points'].mean().nlargest(10).index
			width = df.groupby(by = 'country')['points'].mean().nlargest(10)
			fig, ax = plt.subplots()
			ax.barh(y = y, width = width, color = '#A6182E')
			ax.invert_yaxis()
			ax.yaxis.set_label_position('right')
			ax.yaxis.tick_right()
			ax.set_xlabel('Note moyenne')
			sl.pyplot(fig)

		sl.divider()

		sl.write('**Note moyenne des vins au cours des années**')

		col3, col4, col5 = sl.columns([1,1,1])

		with col3:
			df2 = load_df()
			
			country_options2 = df['country'].drop_duplicates().sort_values().to_list()
			country_options2.insert(0, '-')
			user_country2 = sl.selectbox('Pays', country_options2, key = 'df2country')

		with col4:
			province_options2 = df2.loc[df2['country'] == user_country2]['province'].drop_duplicates().sort_values().to_list()
			user_province2 = sl.selectbox('Région', province_options2, key = 'df2province')
		
		with col5:
			variety_options2 = df2.loc[df2['province'] == user_province2]['variety'].drop_duplicates().sort_values().to_list()
			user_variety2 = sl.selectbox('Cépage', variety_options2, key = 'df2variety')

		if user_country2 != '-':
			df2 = df2.loc[df2['country'] == user_country2]
		if user_province2:
			df2 = df2.loc[df2['province'] == user_province2]
		if user_variety2:
			df2 = df2.loc[df2['variety'] == user_variety2]

		x = df2.groupby(by = 'year')['points'].mean().index
		y = df2.groupby(by = 'year')['points'].mean()
		fig, ax = plt.subplots()
		ax.plot(x, y, marker = ".", color = '#A6182E', label = 'Note moyenne')
		#plt.legend()
		ax.set_ylabel('Note moyenne')
		sl.pyplot(fig)

	with tab2:
		
		col1, col2 = sl.columns([1,1])

		with col1:
			img = Image.open('wc_global.png')
			sl.image(img)

		with col2:
			sl.write("WordCloud du dataset intégral")

		col3, col4 = sl.columns([1,1])

		with col3:
			img = Image.open('wc_fr_pn.png')
			sl.image(img)

		with col4:
			sl.write("WordCloud du dataset filtré (Pinot Noir de Bourgogne)")

		col5, col6 = sl.columns([1,1])

		with col5:
			img = Image.open('wc_client.png')
			sl.image(img)

		with col6:
			sl.write("WordCloud du descriptif sur le Corton Grèves 2016")

	with tab3:

		col1, col2, col3, col4 = sl.columns([1,1,1,1])
		
		with col1:
			df3 = load_df()

			country_options3 = df['country'].drop_duplicates().sort_values().to_list()
			country_options3.insert(0, '-')
			user_country3 = sl.selectbox('Pays', country_options3, key = 'df3country')

		with col2:
			province_options3 = df3.loc[df3['country'] == user_country3]['province'].drop_duplicates().sort_values().to_list()
			user_province3 = sl.selectbox('Région', province_options3, key = 'df3province')
		
		with col3:
			variety_options3 = df3.loc[df3['province'] == user_province3]['variety'].drop_duplicates().sort_values().to_list()
			user_variety3 = sl.selectbox('Cépage', variety_options3, key = 'df3variety')

		with col4:
			year_options3 = df3.loc[(df3['province'] == user_province3) & (df3['variety'] == user_variety3)]['year'].drop_duplicates().sort_values().to_list()
			user_year3 = sl.selectbox('Millésime', year_options3, key = 'df3years')

		if user_country3 != '-':
			df3 = df3.loc[df3['country'] == user_country3]
		if user_province3:
			df3 = df3.loc[df3['province'] == user_province3]
		if user_variety3:
			df3 = df3.loc[df3['variety'] == user_variety3]
		if user_year3:
			df3 = df3.loc[df3['year'] == user_year3]

		describe_table = df3.describe().loc['min':'max'].transpose().iloc[2:3]
		sl.dataframe(describe_table)
		sl.caption("Prix en dollars")

		sl.divider()

		sl.write('**Prix moyen en dollars du Pinot Noir de Bourgogne au cours des années**')
		df_fr_pn = df.loc[(df['country'] == 'France') & (df['province'] == 'Burgundy') & (df['variety'] == 'Pinot Noir')]
		pivot_table = df_fr_pn.pivot_table(columns = 'year',
               index = 'variety',
               values = 'price',
               aggfunc = 'mean')

		sl.dataframe(pivot_table)

	with tab4:
		sl.write("Selon l'analyse du jeu de données, le prix d'un Pinot Noir de Bourgogne 2016 peut atteindre 1600 dollars sur le marché américain. Or, le prix moyen se situe autour de 74 dollars pour ce millésime.")

		sl.write("Le prix des 25 pourcents les plus chers des vins similaires commence à 68,50 dollars. Afin de se positionner sur le haut de gamme, il est ainsi recommandé de s'aligner sur la moyenne.")
