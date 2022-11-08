import pandas as pd

from countries import countries
from words import words

# translate the names of countries
def translate_country(name):
    if name in countries:
        return countries[name]
    return name


# translate the names of commodity groups


def translate(name):
    if name in words:
        return words[name]
    return name


# convert variation
def growth(num):

    return round(num - 100, 1)


# function to process the excel file into a dataframe
def process_world(data):

    """
    Returns all of the data in a dataframe.
    """

    # drop NA values and replace * and - with zeros
    # not necessary for this file

    data.dropna(inplace=True)
    data.replace("*", 0, inplace=True)
    data.replace("-", 0, inplace=True)
    data["Paese"] = data["Naziv"].str.strip()
    data["Paese"] = data["Paese"].apply(lambda x: translate_country(x))

    data["Var. Export"] = pd.to_numeric(data["Indeks - izvoz"])
    data["Var. Import"] = pd.to_numeric(data["Indeks - uvoz"])

    data["Var. Export"] = data["Var. Export"].apply(lambda x: growth(x))
    data["Var. Import"] = data["Var. Import"].apply(lambda x: growth(x))

    data["Esportazioni"] = pd.to_numeric(data["Izvoz"], downcast="integer")
    data["Importazioni"] = pd.to_numeric(data["Uvoz"], downcast="integer")
    data["Interscambio"] = data["Esportazioni"] + data["Importazioni"]
    data["Surplus"] = data["Esportazioni"] - data["Importazioni"]
    data["Var. Interscambio"] = round(
        (
            data["Var. Export"] * data["Esportazioni"]
            + data["Var. Import"] * data["Importazioni"]
        )
        / (data["Esportazioni"] + data["Importazioni"]),
        1,
    )

    data.sort_values(by="Interscambio", inplace=True, ascending=False)
    data = data[
        [
            "Paese",
            "Esportazioni",
            "Importazioni",
            "Var. Export",
            "Var. Import",
            "Interscambio",
            "Surplus",
            "Var. Interscambio",
        ]
    ]

    return data


# function to process the excel file into a dataframe
def proces_italy(data):

    """
    Returns all of the data in a dataframe.
    """

    # drop NA values and replace * and - with zeros
    data.dropna(inplace=True)
    data.replace("*", 0, inplace=True)
    data.replace("-", 0, inplace=True)
    data["Voce"] = data["Naziv"].str.strip()
    data["Voce"] = data["Voce"].apply(lambda x: translate(x))

    data["Var. Export"] = pd.to_numeric(data["Indeks - izvoz"])
    data["Var. Import"] = pd.to_numeric(data["Indeks - uvoz"])

    data["Var. Export"] = data["Var. Export"].apply(lambda x: growth(x))
    data["Var. Import"] = data["Var. Import"].apply(lambda x: growth(x))

    data["Esportazioni"] = pd.to_numeric(data["Izvoz"], downcast="integer")
    data["Importazioni"] = pd.to_numeric(data["Uvoz"], downcast="integer")
    data["Interscambio"] = data["Esportazioni"] + data["Importazioni"]
    data["Surplus"] = data["Esportazioni"] - data["Importazioni"]

    data["Var. Interscambio"] = round(
        (
            data["Var. Export"] * data["Esportazioni"]
            + data["Var. Import"] * data["Importazioni"]
        )
        / (data["Esportazioni"] + data["Importazioni"]),
        1,
    )

    data = data[
        [
            "Voce",
            "Esportazioni",
            "Importazioni",
            "Var. Export",
            "Var. Import",
            "Interscambio",
            "Surplus",
            "Var. Interscambio",
        ]
    ]

    # debug: uncomment the following line to inspect the df
    # st.write(data)
    return data
