"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel
import glob
import os
import pandas as pd


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    output_dir = "files/output"
    os.makedirs(output_dir, exist_ok=True)

    input_files = glob.glob("files/input/*.csv.zip")
    if not input_files:
        return

    df_list = [pd.read_csv(file) for file in input_files]
    df = pd.concat(df_list, ignore_index=True)

    client_df = df[
        ["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]
    ].copy()
    
    client_df = client_df.rename(columns={"mortgage": "mortgage"})

    client_df["job"] = (
        client_df["job"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )
    
    client_df["education"] = (
        client_df["education"]
        .astype(str)
        .str.replace(".", "_", regex=False)
        .replace("unknown", pd.NA)
    )

    client_df["credit_default"] = client_df["credit_default"].apply(
        lambda x: 1 if str(x).lower() == "yes" else 0
    )
    client_df["mortgage"] = client_df["mortgage"].apply(
        lambda x: 1 if str(x).lower() == "yes" else 0
    )

    client_df.to_csv(os.path.join(output_dir, "client.csv"), index=False)

    months_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }

    def parse_date(row):
        day = str(row["day"]).zfill(2)
        month_str = str(row["month"]).lower()[:3]
        month = months_map.get(month_str, "01")
        return f"2022-{month}-{day}"

    df["last_contact_date"] = df.apply(parse_date, axis=1)

    campaign_df = df[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts", 
            "previous_outcome",
            "campaign_outcome",
            "last_contact_date",
        ]
    ].copy()

    campaign_df["previous_outcome"] = campaign_df["previous_outcome"].apply(
        lambda x: 1 if str(x).lower() == "success" else 0
    )
    campaign_df["campaign_outcome"] = campaign_df["campaign_outcome"].apply(
        lambda x: 1 if str(x).lower() == "yes" else 0
    )

    campaign_df.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)

    economics_df = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    economics_df.columns = ["client_id", "cons_price_idx", "euribor_three_months"]

    economics_df.to_csv(os.path.join(output_dir, "economics.csv"), index=False)

    return


if __name__ == "__main__":
    clean_campaign_data()
