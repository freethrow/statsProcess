import streamlit as st
import pandas as pd

# st.set_page_config(layout="wide")

st.title("Commercio Estero della Serbia")


# Serbia - World data
world_data = pd.read_excel("Serbia-Mondo.xlsx", index_col=None)

st.write(world_data)

st.bar_chart(
    data=world_data[world_data["Paese"] != "TOTALE"].sort_values(
        ["Esportazioni"], ascending=False
    ),
    x="Paese",
    y="Esportazioni",
)

st.bar_chart(
    data=world_data[world_data["Paese"] != "TOTALE"].sort_values(
        ["Importazioni"], ascending=False
    ),
    x="Paese",
    y="Importazioni",
)

st.bar_chart(
    data=world_data[world_data["Paese"] != "TOTALE"].sort_values(
        ["Interscambio"], ascending=False
    ),
    x="Paese",
    y="Interscambio",
)
