import matplotlib.pyplot as plt

def bar_plot(df, pagina, color, n, m2, kind):
    dfb = df.sort_values(by="Precio_2022", ascending=True).head(n)

    addi = "/m²"
    if kind == "Total":
        dfb["Precio_2022"] = dfb["Precio_2022"]*m2
        addi = ""
    
    fig, ax = plt.subplots()
    
    ax.bar(dfb["Barrio"], dfb["Precio_2022"], color = color)
    
    ax.set_xlabel("Neighborhood")
    ax.set_ylabel(f"Price (€{addi})")
    ax.set_title(f"Top {n} cheapest neighborhoods in {pagina}")

    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return(fig)
