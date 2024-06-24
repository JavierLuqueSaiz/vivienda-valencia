import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def load_compra():
    df_fotocasa = pd.read_csv("ficheros/precio-de-compra-en-fotocasa.csv", delimiter=";")
    df_fotocasa = df_fotocasa.dropna(subset=["Precio_2022 (Euros/m2)"])
    barrios_fotocasa = list(df_fotocasa.sort_values(by="BARRIO").BARRIO)
    df_idealista = pd.read_csv("ficheros/precio-de-compra-en-idealista.csv", delimiter=";")
    df_idealista = df_idealista.dropna(subset=["Precio_2022 (Euros/m2)"])
    barrios_idealista = list(df_idealista.sort_values(by="BARRIO").BARRIO)
    barrios = dict(zip(barrios_fotocasa, barrios_idealista))
    for barrio in barrios_fotocasa:
        df_fotocasa.loc[df_fotocasa["BARRIO"] == barrio, "BARRIO"] = barrios[barrio]
    merged_df = pd.merge(df_idealista,
                        df_fotocasa,
                        on=['BARRIO', "Geo Point", "Geo Shape", "DISTRITO"],
                        how='outer', suffixes=('_idealista', '_fotocasa')) \
        .sort_values(by="BARRIO")

    merged_df = merged_df.drop(columns=["coddistbar_idealista",
                                        "codbarrio_idealista",
                                        "coddistrit_idealista",
                                        "Fecha_creacion_idealista",
                                        "coddistbar_fotocasa",
                                        "codbarrio_fotocasa",
                                        "coddistrit_fotocasa",
                                        "Fecha_creacion_fotocasa"])

    cols = ["GeoPoint",
            "GeoShape",
            "Barrio",
            "Distrito",
            "Precio_2022_idealista",
            "Precio_2010_idealista",
            "Precio_max_idealista",
            "Año_max_idealista",
            "Precio_2022_fotocasa",
            "Precio_2010_fotocasa",
            "Precio_max_fotocasa",
            "Año_max_fotocasa",]
    merged_df.columns = cols

    scaler = MinMaxScaler(feature_range=(0.3,1))

    merged_df['opacity_idealista'] = scaler.fit_transform(merged_df[['Precio_2022_idealista']])
    merged_df['opacity_fotocasa'] = scaler.fit_transform(merged_df[['Precio_2022_fotocasa']])

    return merged_df

def añadir_coordenadas(df):
    df_merged = load_compra()
    df_merged = df_merged.sort_values(by="Barrio").reset_index(drop=True)
    df = df.sort_values(by="Barrio").reset_index(drop=True)
    df["GeoPoint"] = df_merged[["GeoPoint"]]
    df["GeoShape"] = df_merged[["GeoShape"]]
    print(list(df["GeoPoint"]) != list(df_merged[["GeoPoint"]]))
    print(list(df["GeoShape"]) != list(df_merged[["GeoShape"]]))
    return df


def asignar_opacity(df, color):
    mask = df['color'] == color
    if color == 'red':
        scaler = MinMaxScaler(feature_range=(0.3,1))
        scaled_values = scaler.fit_transform(df.loc[mask, 'Precio_2022'].values.reshape(-1, 1)).flatten()
    elif color == 'yellow':
        scaled_values = np.full(df[mask].shape[0], 0.5)
    elif color == 'green':
        scaler = MinMaxScaler(feature_range=(0,0.7))
        scaled_values = 1 - scaler.fit_transform(df.loc[mask, 'Precio_2022'].values.reshape(-1, 1)).flatten()
    df.loc[mask, 'opacity'] = scaled_values

def load_alquiler():
    df = pd.read_csv("ficheros/precio-alquiler-vivienda.csv", delimiter=";")

    df = df.drop(columns=["CodBar-CodDistrit"])

    cols = ["Distrito",
            "Barrio",
            "Precio_2022",
            "Precio_2010",
            "Precio_max",
            "Año_max"]
    
    df.columns = cols

    df['color'] = pd.qcut(df['Precio_2022'], q=3, labels=['green', 'yellow', 'red'])

    asignar_opacity(df, 'red')
    asignar_opacity(df, 'yellow')
    asignar_opacity(df, 'green')

    df = añadir_coordenadas(df)

    print(df)
    
    return df
