import folium
import streamlit as st
from streamlit_folium import st_folium
from utils.data import load_compra, load_alquiler
from utils.maps import add_polygon
from utils.buttons import compra_venta, fotocasa_idealista, metros_cuadrados
from utils.explanations import rent, buy
from utils.graphics import bar_plot

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
else:

    st.title('House Map Price in Valencia')

    if option == "Buy":
        html_code = buy()
    else:
        html_code = rent()

    st.markdown(html_code, unsafe_allow_html=True)

    if option == "Buy":
        pagina = pagina[0]
        df["Precio_2022"] = df[f"Precio_2022_{pagina.lower()}"]
        if pagina == "Idealista":
            color = "red"
        else:
            color = "blue"
    else:
        color = "green"

    st_folium(m, width=850, height=700)

    st.title('Bar plot of cheapest neighborhoods')

    n = st.number_input("Number of neighborhoods",  min_value=0, max_value=70, value=10, step=1)

    kind = st.radio(
        label="Select a display type",
        options=["Per m²", "Total"]
    )

    if option == "Rent":
        st.markdown("Keep in mind that the data for renting is the same for both web pages.")
    else:
        st.markdown("The prices of the first selected web page will be shown.")

    st.pyplot(bar_plot(df, pagina, color, n, m2, kind))