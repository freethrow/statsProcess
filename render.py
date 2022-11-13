from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

from pathlib import Path

import pandas as pd

import json

doc = DocxTemplate("template/template.docx")

TOP_N = 10


def to_currency(row):
    row["esp_currency"] = "{:,.0f},000 EUR".format(float(row["Esportazioni"]))
    row["imp_currency"] = "{:,.0f},000 EUR".format(float(row["Importazioni"]))
    row["int_currency"] = "{:,.0f},000 EUR".format(float(row["Interscambio"]))
    return row


def num_to_curr(value):
    return "{:,.0f},000 EUR".format(float(value))


def render_doc(world_data, italy_data, report_name):

    # add totals for world and italy

    total_world = {
        "serbian_export_world":
        num_to_curr(world_data[world_data["Paese"] == "TOTALE"]
                    ["Esportazioni"].values[0]),
        "serbian_import_world":
        num_to_curr(world_data[world_data["Paese"] == "TOTALE"]
                    ["Importazioni"].values[0]),
        "serbian_export_world_rate":
        round(
            world_data[world_data["Paese"] == "TOTALE"]
            ["Var. Export"].values[0], 1),
        "serbian_import_world_rate":
        round(
            world_data[world_data["Paese"] == "TOTALE"]
            ["Var. Import"].values[0], 1),
    }

    world_data = world_data.apply(to_currency, axis=1)
    to_append_world = world_data[world_data["Paese"] == "TOTALE"]
    world_data = world_data[world_data["Paese"] != "TOTALE"]

    # separate tables for export, import and exchange
    export_tbl = world_data.sort_values(by="Esportazioni", ascending=False)[[
        "Paese", "esp_currency", "Var. Export"
    ]].head(TOP_N)

    export_tbl = pd.concat([
        export_tbl, to_append_world[["Paese", "esp_currency", "Var. Export"]]
    ])

    import_tbl = world_data.sort_values(by="Importazioni", ascending=False)[[
        "Paese", "imp_currency", "Var. Import"
    ]].head(TOP_N)

    import_tbl = pd.concat([
        import_tbl, to_append_world[["Paese", "imp_currency", "Var. Import"]]
    ])

    exchange_tbl = world_data.sort_values(by="Interscambio", ascending=False)[[
        "Paese", "int_currency", "Var. Interscambio"
    ]].head(TOP_N)

    exchange_tbl = pd.concat([
        exchange_tbl,
        to_append_world[["Paese", "int_currency", "Var. Interscambio"]]
    ])

    export_pic = InlineImage(
        doc,
        image_descriptor="output/world-Esportazioni.png",
        width=Mm(180),
        height=Mm(120),
    )
    import_pic = InlineImage(
        doc,
        image_descriptor="output/world-Importazioni.png",
        width=Mm(180),
        height=Mm(120),
    )
    exchange_pic = InlineImage(
        doc,
        image_descriptor="output/world-Interscambio.png",
        width=Mm(180),
        height=Mm(120),
    )

    italy_data = italy_data.apply(to_currency, axis=1)

    to_append_italy = italy_data[italy_data["Voce"] == "TOTALE"]

    italy_data = italy_data[italy_data["Voce"] != "TOTALE"]

    # separate tables for export, import and exchange
    export_tbl_it = italy_data.sort_values(
        by="Esportazioni",
        ascending=False)[["Voce", "esp_currency", "Var. Export"]].head(TOP_N)

    export_tbl_it = pd.concat([
        export_tbl_it, to_append_italy[["Voce", "esp_currency", "Var. Export"]]
    ])

    import_tbl_it = italy_data.sort_values(
        by="Importazioni",
        ascending=False)[["Voce", "imp_currency", "Var. Import"]].head(TOP_N)

    import_tbl_it = pd.concat([
        import_tbl_it, to_append_italy[["Voce", "imp_currency", "Var. Import"]]
    ])

    exchange_tbl_it = italy_data.sort_values(by="Interscambio",
                                             ascending=False)[[
                                                 "Voce", "int_currency",
                                                 "Var. Interscambio"
                                             ]].head(TOP_N)

    exchange_tbl_it = pd.concat([
        exchange_tbl_it,
        to_append_italy[["Voce", "int_currency", "Var. Interscambio"]]
    ])

    export_pic_it = InlineImage(
        doc,
        image_descriptor="output/italy-Esportazioni.png",
        width=Mm(180),
        height=Mm(120),
    )
    import_pic_it = InlineImage(
        doc,
        image_descriptor="output/italy-Importazioni.png",
        width=Mm(180),
        height=Mm(120),
    )
    exchange_pic_it = InlineImage(
        doc,
        image_descriptor="output/italy-Interscambio.png",
        width=Mm(180),
        height=Mm(120),
    )

    context = {
        "report_name": report_name,
        "export_rows": json.loads(export_tbl.to_json(orient="records")),
        "import_rows": json.loads(import_tbl.to_json(orient="records")),
        "exchange_rows": json.loads(exchange_tbl.to_json(orient="records")),
        "export_pic": export_pic,
        "import_pic": import_pic,
        "exchange_pic": exchange_pic,
        "export_rows_it": json.loads(export_tbl_it.to_json(orient="records")),
        "import_rows_it": json.loads(import_tbl_it.to_json(orient="records")),
        "exchange_rows_it":
        json.loads(exchange_tbl_it.to_json(orient="records")),
        "export_pic_it": export_pic_it,
        "import_pic_it": import_pic_it,
        "exchange_pic_it": exchange_pic_it,
        "serbian_export": total_world["serbian_export_world"],
        "serbian_import": total_world["serbian_import_world"],
        "serbian_export_rate": total_world["serbian_export_world_rate"],
        "serbian_import_rate": total_world["serbian_import_world_rate"],
    }
    doc.render(context)

    output_name = f"output/ReportCommercio{report_name}.docx"

    doc.save(output_name)

    from docx2pdf import convert

    convert(output_name)
