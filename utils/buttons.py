import streamlit as st  

def compra_venta():
    # Definir las opciones de selección
    option = st.sidebar.radio(
        label="What are you looking for?",
        options=["Buy", "Rent"],
    )

    return option

def fotocasa_idealista(option):
    options = ["Fotocasa", "Idealista"]
    if option == "Buy":
        pagina = st.sidebar.multiselect(
            label="What pages do you want to search?",
            options=options,
            default=options
        )
    else:
        pagina = st.sidebar.radio(
            label="What pages do you want to search?",
            options=options
        )
    return pagina

def metros_cuadrados():
    m2 = st.sidebar.number_input("How many squared meters are you looking for?", min_value=0, max_value=500, value=90, step=1)
    return m2