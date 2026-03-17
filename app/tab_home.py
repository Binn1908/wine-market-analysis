import streamlit as sl
from PIL import Image

sl.set_page_config(layout = 'wide')

def tab_home():
	sl.title('Bienvenue')

	img = Image.open('vigne.png')
	sl.image(img)
