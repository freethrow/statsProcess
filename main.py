import typer

from pathlib import Path

from rich import print
import pandas as pd

from email_validator import validate_email, EmailNotValidError

from process import proces_italy, process_world
from create_charts import chart_world
from render import render_doc


def main(email: str = typer.Argument(None)):

    if email:
        print("Sending report to:", email)

        try:
            # Check that the email address is valid.
            validation = validate_email(email)

        except EmailNotValidError as e:
            # Email is not valid.
            # The exception message is human-readable.
            print(str(e))

    else:
        print("Not sending email")

    # check for existance of files otherwise exit

    world_stats = "input\IT20 EU.xls"
    italy_stats = "input\IT ODSEK.xls"

    world_present = Path(world_stats).is_file()
    italy_present = Path(italy_stats).is_file()

    if world_present and italy_present:
        print("Files present. Ok!")

        # process world stats
        print("Processing world statistics...")
        world_data = read_world_stats(world_stats)

        # process italy stats
        print("Processing Italy statistics...")
        italy_data = read_italy_stats(italy_stats)

        print("Rendering report...")
        rendered = render_doc(world_data=world_data,
                              italy_data=italy_data,
                              report_name=get_period(world_stats))

        if (rendered and email):
            from mail import send_report
            send_report(HTMLcontent="<h2>Report statistica</h2>",
                        reportName='report-2022-11-13.zip',
                        email=email)

    else:
        print(
            f"There must be exactly two excel files named {world_stats} and {italy_stats}"
        )
        raise typer.Exit()


def get_period(filename):
    header = pd.read_excel(filename,
                           index_col=None,
                           usecols="A",
                           header=1,
                           nrows=0)

    full_header = header.columns.values[0]
    period = full_header.split("PERIOD")[1].split("20 naj")[0][:-1]

    return period


def read_world_stats(world_stats):

    w_data_exp = pd.read_excel(world_stats,
                               sheet_name="izvoz",
                               skiprows=2,
                               usecols="A:F").dropna()

    w_data_imp = pd.read_excel(world_stats,
                               sheet_name="uvoz",
                               skiprows=2,
                               usecols="A:F").dropna()

    # concatenate the dataframes
    w_data = pd.concat([w_data_exp, w_data_imp],
                       ignore_index=True).drop_duplicates(ignore_index=True)

    # save to excel file
    final_world = process_world(w_data)

    chart_world(final_world)
    chart_world(data=final_world, value="Importazioni")
    chart_world(data=final_world, value="Interscambio")

    final_world.to_excel("output/Serbia-Mondo.xlsx", index=False)

    return final_world


def read_italy_stats(italy_stats):

    italy_data = pd.read_excel(italy_stats, skiprows=2, usecols="B:F")
    final_italy = proces_italy(italy_data)

    # create charts
    chart_world(final_italy, world=False)
    chart_world(data=final_italy, value="Importazioni", world=False)
    chart_world(data=final_italy, value="Interscambio", world=False)

    # save to excel file
    final_italy.to_excel("output/Serbia-Italia.xlsx", index=False)

    return final_italy


if __name__ == "__main__":
    typer.run(main)
