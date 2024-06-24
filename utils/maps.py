import folium
import json

def add_marker(m, coords, text="", url=""):
    html = f"""
        <div style="color: black; text-align: center;">
            <a href="{url}" target="_blank">
                <i class="fa fa-info-circle fa-2x" style="color: black";"></i>
            </a>
        </div>
    """
    
    folium.map.Marker(coords,
                      icon=folium.DivIcon(html=html),
                      tooltip=text
                      ).add_to(m)
    return m

def selecter(row, option, pagina):
    if not pagina:
        return None, None, None, None, None
    if option == "Buy" and len(pagina) == 2:
        if row["Precio_2022_idealista"] < row["Precio_2022_fotocasa"]:
            return select_page(row, "Idealista", option)
        return select_page(row, "Fotocasa", option)
    if isinstance(pagina, list):
        pagina = pagina[0]
    return select_page(row, pagina, option)

def select_page(row, pagina, option):
    if pagina == "Idealista":
        if option == "Buy":
            sufijo = "_" + pagina.lower()
            color = "red"
            tipo = "venta"
        else:
            color = row["color"]
            sufijo = ""
            tipo = "alquiler"
        pagina = "Idealista"
        precio = row[f"Precio_2022{sufijo}"]
        opacity = row[f'opacity{sufijo}']

        barrio = row['Barrio'].lower() \
            .replace("\'","-") \
            .replace(" ", "-") \
            .replace("llorens", "llorenc") \
            .replace("la-malva-rosa", "playa-de-la-malvarrosa") \
            .replace("cabanyal-canyamelar", "el-cabanyal-el-canyamelar") \
            .replace("la-gran-via", "gran-via") \
            .replace(".", "") \
            .replace("la-fonteta-slluis", "fonteta-de-sant-lluis")
        distrito = row['Distrito'].lower() \
            .replace("\'","-") \
            .replace(" ", "-")
        url = f"https://www.idealista.com/{tipo}-viviendas/valencia/{distrito}/{barrio}/"
    else:
        if option == "Buy":
            sufijo = "_" + pagina.lower()
            color = "blue"
            tipo = "comprar"
        else:
            color = row["color"]
            sufijo = ""
            tipo = "alquiler"
        pagina = "Fotocasa"
        precio = row[f"Precio_2022{sufijo}"]
        opacity = row[f'opacity{sufijo}']

        barrio = row['Barrio'].lower() \
            .replace("\'","") \
            .replace(" ", "-") \
            .replace("llorens", "llorenc")
        distrito = row['Distrito'].lower() \
            .replace("\'","") \
            .replace(" ", "-")
        url = f"https://www.fotocasa.es/es/{tipo}/viviendas/valencia-capital/{barrio}/l"

    return color, precio, opacity, url, pagina

def show_price(p, option):
    if option == "Buy":
        return f"{int(p):,}".replace(",",".")
    else:
        return f"{p:.2f}".replace(".", ",")

def add_polygon(m, row, option, pagina, m2):
    color, precio, opacity, url, pagina = selecter(row, option, pagina)
    if color:
        text = f"""
            <div style="line-height:1.5;">
            <strong>Webpage:</strong> {pagina}<br>
            <strong>Neighbourhood:</strong> {row["Barrio"].capitalize()}<br>
            <strong>Total price:</strong> {show_price(precio*m2,option)} €<br>
            <strong>Price:</strong> {show_price(precio,option)} €/m²
            </div>
        """

        map_center = row["GeoPoint"].split(", ")
        geojson_str = row["GeoShape"]
        geojson_data = json.loads(geojson_str)
        folium.GeoJson(
            geojson_data,
            style_function=lambda x, color=color, opacity=opacity: {
                'color': "black",
                'fillColor': color,
                'fillOpacity': opacity
            }
        ).add_to(m)

        add_marker(m, map_center, text=text, url=url)
    else:
        return "ERROR"