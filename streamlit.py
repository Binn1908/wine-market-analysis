from pathlib import Path

from PIL import Image
import streamlit as st

from app.tab_analyse import tab_analyse
from app.tab_home import tab_home
from app.tab_presentation import tab_presentation

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

st.set_page_config(layout="wide")

tabs = {"Home": tab_home, "Présentation": tab_presentation, "Analyse": tab_analyse}

with st.sidebar:
    st.image(Image.open(ASSETS / "logo.png"), width=250)
    tab_selection = st.radio("Menu", list(tabs.keys()))

tabs[tab_selection]()

st.divider()

st.markdown(
    "**Le Domaine des Croix — Etude de marché** · "
    "Réalisé par [Chinnawat Wisetwongsa](https://linkedin.com/in/wisetwongsa/)"
)
