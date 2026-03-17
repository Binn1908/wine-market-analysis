from pathlib import Path

from PIL import Image
import streamlit as st

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"


def tab_home():
    st.title("Bienvenue")

    st.image(Image.open(ASSETS / "vigne.png"))
