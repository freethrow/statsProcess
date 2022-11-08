from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

from pathlib import Path

import json

doc = DocxTemplate("template/template.docx")

TOP_N = 10


def render_doc(world_data, italy_data):

    world_data = world_data[world_data["Paese"] != "TOTALE"]

    def to_currency(row):
        row["esp_currency"] = "{:,.0f},000 EUR".format(float(row["Esportazioni"]))
        row["imp_currency"] = "{:,.0f},000 EUR".format(float(row["Importazioni"]))
        row["int_currency"] = "{:,.0f},000 EUR".format(float(row["Interscambio"]))
        return row

    world_data = world_data.apply(to_currency, axis=1)

    # separate tables for export, import and exchange
    export_tbl = world_data.sort_values(by="Esportazioni", ascending=False)[
        ["Paese", "esp_currency", "Var. Export"]
    ].head(TOP_N)

    import_tbl = world_data.sort_values(by="Importazioni", ascending=False)[
        ["Paese", "imp_currency", "Var. Import"]
    ].head(TOP_N)

    exchange_tbl = world_data.sort_values(by="Interscambio", ascending=False)[
        ["Paese", "int_currency", "Var. Interscambio"]
    ].head(TOP_N)

    export_pic = InlineImage(
        doc, image_descriptor="world-Esportazioni.png", width=Mm(180), height=Mm(120)
    )
    import_pic = InlineImage(
        doc, image_descriptor="world-Importazioni.png", width=Mm(180), height=Mm(120)
    )
    exchange_pic = InlineImage(
        doc, image_descriptor="world-Interscambio.png", width=Mm(180), height=Mm(120)
    )

    italy_data = italy_data[italy_data["Voce"] != "TOTALE"]

    italy_data = italy_data.apply(to_currency, axis=1)
    # separate tables for export, import and exchange
    export_tbl_it = italy_data.sort_values(by="Esportazioni", ascending=False)[
        ["Voce", "esp_currency", "Var. Export"]
    ].head(TOP_N)

    import_tbl_it = italy_data.sort_values(by="Importazioni", ascending=False)[
        ["Voce", "imp_currency", "Var. Import"]
    ].head(TOP_N)

    exchange_tbl_it = italy_data.sort_values(by="Interscambio", ascending=False)[
        ["Voce", "int_currency", "Var. Interscambio"]
    ].head(TOP_N)

    export_pic_it = InlineImage(
        doc, image_descriptor="italy-Esportazioni.png", width=Mm(180), height=Mm(120)
    )
    import_pic_it = InlineImage(
        doc, image_descriptor="italy-Importazioni.png", width=Mm(180), height=Mm(120)
    )
    exchange_pic_it = InlineImage(
        doc, image_descriptor="italy-Interscambio.png", width=Mm(180), height=Mm(120)
    )

    context = {
        "export_rows": json.loads(export_tbl.to_json(orient="records")),
        "import_rows": json.loads(import_tbl.to_json(orient="records")),
        "exchange_rows": json.loads(exchange_tbl.to_json(orient="records")),
        "export_pic": export_pic,
        "import_pic": import_pic,
        "exchange_pic": exchange_pic,
        "export_rows_it": json.loads(export_tbl_it.to_json(orient="records")),
        "import_rows_it": json.loads(import_tbl_it.to_json(orient="records")),
        "exchange_rows_it": json.loads(exchange_tbl_it.to_json(orient="records")),
        "export_pic_it": export_pic_it,
        "import_pic_it": import_pic_it,
        "exchange_pic_it": exchange_pic_it,
    }
    doc.render(context)

    doc.save("generated_doc.docx")

    from docx2pdf import convert

    convert("generated_doc.docx")
