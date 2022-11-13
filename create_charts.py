import plotly.express as px
from plotly import io as pio


def chart_world(data, top=10, value="Esportazioni", world=True):

    if value == "Esportazioni":
        color = "Var. Export"
    elif value == "Importazioni":
        color = "Var. Import"
    elif value == "Interscambio":
        color = "Var. Interscambio"

    if world:
        chart_data = (
            data[data["Paese"] != "TOTALE"]
            .sort_values([value], ascending=False)
            .head(20)
        )
        x = "Paese"
        title = f"{value} della Serbia - principali Paesi partner (valori in 1000 EUR)"
    else:
        chart_data = (
            data[data["Voce"] != "TOTALE"]
            .sort_values([value], ascending=False)
            .head(20)
        )
        x = "Voce"
        title = (
            f"{value} della Serbia - con Italia principali voci (valori in 1000 EUR)"
        )

    # create plot
    fig = px.bar(
        chart_data,
        x=x,
        y=value,
        color=color,
        color_continuous_scale="deep",
        title=title,
    )

    # export as static image
    filename = value + ".png"
    if world:
        filename = "output/world-" + filename
    else:
        filename = "output/italy-" + filename
    pio.write_image(fig, filename)
