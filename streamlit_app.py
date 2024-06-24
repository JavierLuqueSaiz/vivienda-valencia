import folium
import streamlit as st
from streamlit_folium import st_folium
from utils.data import load_compra, load_alquiler
from utils.maps import add_polygon
from utils.buttons import compra_venta, fotocasa_idealista, metros_cuadrados
from utils.explanations import rent, buy

option = compra_venta()
pagina = fotocasa_idealista(option)
m2 = metros_cuadrados()

if option == "Buy":
    df = load_compra()
else:
    df = load_alquiler()

m = folium.Map(location=[39.46975, -0.35139], zoom_start=13)

for index, row in df.iterrows():
    x = add_polygon(m, row, option, pagina, m2)
if x == "ERROR":
    st.error("Select at least one page")

st.title('House Map Price in Valencia')

if option == "Buy":
    html_code = buy()
else:
    html_code = rent()

st.markdown(html_code, unsafe_allow_html=True)


st_folium(m, width=850, height=700)