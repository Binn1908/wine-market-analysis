from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
ASSETS = ROOT / "assets"


@st.cache_data
def load_df():
    df1 = pd.read_pickle(DATA / "df_clean1.pickle")
    df2 = pd.read_pickle(DATA / "df_clean2.pickle")
    df3 = pd.read_pickle(DATA / "df_clean3.pickle")
    df4 = pd.read_pickle(DATA / "df_clean4.pickle")
    df = pd.concat([df1, df2, df3, df4])
    return df


def tab_analyse():
    df = load_df()

    st.title("Analyse")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Analyse exploratoire", "Descriptions", "Comparateur de prix", "Conseil"]
    )

    with tab1:
        st.subheader("Note moyenne par pays")
        df_country = df.groupby(by=["country", "code"], as_index=False)["points"].mean()
        fig = px.choropleth(
            df_country,
            locations="code",
            color="points",
            color_continuous_scale=[[0, "rgb(255,255,255)"], [1, "rgb(166,24,46)"]],
            hover_name="country",
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top 10 - Les pays les mieux notés")
            top_countries = df.groupby("country")["points"].mean().nlargest(10)
            fig, ax = plt.subplots(figsize=(4,5))
            ax.barh(y=top_countries.index, width=top_countries.values, color="#A6182E")
            ax.invert_yaxis()
            ax.set_xlabel("Note moyenne")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with col2:
            st.subheader("Top 10 - Répartition des vins par pays")
            top_counts = df.country.value_counts().nlargest(10)
            fig, ax = plt.subplots()
            ax.pie(top_counts.values, labels=top_counts.index, autopct="%1.1f%%")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.divider()

        st.subheader("Note moyenne des vins au cours des années")

        df_filtered = df.copy()

        col3, col4, col5 = st.columns(3)

        with col3:
            country_options = df["country"].drop_duplicates().sort_values().to_list()
            country_options.insert(0, "-")
            user_country = st.selectbox("Pays", country_options, key="tab1_country")

        with col4:
            province_options = (
                df.loc[df["country"] == user_country]["province"]
                .drop_duplicates()
                .sort_values()
                .to_list()
            )
            user_province = st.selectbox(
                "Région", province_options, key="tab1_province"
            )

        with col5:
            variety_options = (
                df.loc[df["province"] == user_province]["variety"]
                .drop_duplicates()
                .sort_values()
                .to_list()
            )
            user_variety = st.selectbox("Cépage", variety_options, key="tab1_variety")

        if user_country != "-":
            df_filtered = df_filtered.loc[df_filtered["country"] == user_country]
        if user_province:
            df_filtered = df_filtered.loc[df_filtered["province"] == user_province]
        if user_variety:
            df_filtered = df_filtered.loc[df_filtered["variety"] == user_variety]

        year_points = df_filtered.groupby("year")["points"].mean()
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(
            year_points.index,
            year_points.values,
            marker=".",
            color="#A6182E",
            label="Note moyenne",
        )
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with tab2:
        st.image(Image.open(ASSETS / "wc_global.png"), width=450)
        st.write("**WordCloud du dataset intégral**")

        st.image(Image.open(ASSETS / "wc_fr_pn.png"), width=450)
        st.write("**WordCloud du dataset filtré (Pinot Noir de Bourgogne)**")

        st.image(Image.open(ASSETS / "wc_client.png"), width=450)
        st.write("**WordCloud du descriptif sur le Corton Grèves 2016**")

    with tab3:
        df_filtered_price = df.copy()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            country_options_price = (
                df["country"].drop_duplicates().sort_values().to_list()
            )
            country_options_price.insert(0, "-")
            user_country_price = st.selectbox(
                "Pays", country_options_price, key="tab3_country"
            )

        with col2:
            province_options_price = (
                df.loc[df["country"] == user_country_price]["province"]
                .drop_duplicates()
                .sort_values()
                .to_list()
            )
            user_province_price = st.selectbox(
                "Région", province_options_price, key="tab3_province"
            )

        with col3:
            variety_options_price = (
                df.loc[df["province"] == user_province_price]["variety"]
                .drop_duplicates()
                .sort_values()
                .to_list()
            )
            user_variety_price = st.selectbox(
                "Cépage", variety_options_price, key="tab3_variety"
            )

        with col4:
            year_options_price = (
                df.loc[
                    (df["province"] == user_province_price)
                    & (df["variety"] == user_variety_price)
                ]["year"]
                .drop_duplicates()
                .sort_values()
                .to_list()
            )
            user_year_price = st.selectbox(
                "Millésime", year_options_price, key="tab3_years"
            )

        if user_country_price != "-":
            df_filtered_price = df_filtered_price.loc[
                df_filtered_price["country"] == user_country_price
            ]
        if user_province_price:
            df_filtered_price = df_filtered_price.loc[
                df_filtered_price["province"] == user_province_price
            ]
        if user_variety_price:
            df_filtered_price = df_filtered_price.loc[
                df_filtered_price["variety"] == user_variety_price
            ]
        if user_year_price:
            df_filtered_price = df_filtered_price.loc[
                df_filtered_price["year"] == user_year_price
            ]

        describe_table = (
            df_filtered_price.describe().loc["min":"max"].transpose().iloc[2:3]
        )
        st.dataframe(describe_table)
        st.caption("Prix en dollars")

        st.divider()

        st.subheader(
            "Prix moyen en dollars du Pinot Noir de Bourgogne au cours des années"
        )
        df_fr_bg_pn = df.loc[
            (df["country"] == "France")
            & (df["province"] == "Burgundy")
            & (df["variety"] == "Pinot Noir")
        ]
        pivot_table = df_fr_bg_pn.pivot_table(
            columns="year", index="variety", values="price", aggfunc="mean"
        ).round(2)
        pivot_table.columns = pivot_table.columns.astype("Int64")
        st.dataframe(pivot_table)

    with tab4:
        st.subheader("Recommandation tarifaire")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="Prix maximum (Pinot Noir Bourgogne 2016)", value="1 590 $")

        with col2:
            st.metric(label="Prix moyen (Pinot Noir Bourgogne 2016)", value="74 $")

        st.success(
            "💡 Recommandation : Afin de se positionner sur le haut de gamme du marché américain, "
            "il est conseillé de fixer un prix autour de 74 dollars, soit dans la moyenne des "
            "Pinot Noir de Bourgogne 2016. Le prix du premier quartile supérieur commence à 68,50 dollars."
        )
