
def buy():
    html_code = """
    <style>
        .fotocasa {
            color: blue;
        }
        .idealista {
            color: red;
        }
    </style>
    <div class="explanation-buy">
        <p>This map displays the average house purchase prices based on the selected platform. If both <span class="fotocasa">Fotocasa</span> and <span class="idealista">Idealista</span> are chosen, the neighborhood's fill color will correspond to the preferred platform for finding your home.</p>
        <p>If you click on any neighborhood, it will take you to the selected webpage with the search results for that neighborhood.</p>
    </div>

    """

    return html_code

def rent():
    html_code = """
    <style>
    .gradient-bar {
        position: relative;
        width: 45%;
        height: 40px;
        margin: 5px auto;
        background: linear-gradient(
            to right, 
            rgba(214, 39, 40, 1) 0%, 
            rgba(214, 39, 40, 0.3) 25%, 
            rgba(255, 255, 0, 0.5) 50%, 
            rgba(44, 160, 44, 0.3) 75%, 
            rgba(44, 160, 44, 1) 100%
        );
        display: flex;
        align-items: center; /* Centrar verticalmente */
        justify-content: space-between; /* Espacio entre los textos */
        padding: 0 10px; /* Espaciado interior */
    }

    .gradient-bar p {
        margin: 0;
        padding: 1px;
        font-size: 14px;
        font-weight: bold;
    }

    </style>
    <div class="explanation-rent">
        <p>This map displays the average house rental prices. Clicking on any neighborhood will direct you to the selected webpage with the search results for that neighborhood. Each neighborhood is color-coded based on its rental price as per the following legend:</p>
    </div>
    <div class="gradient-bar">
        <p class="more">More Expensive</p>
        <p class="less">Less Expensive</p>
    </div>
    """

    return html_code
