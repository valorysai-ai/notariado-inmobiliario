import json
import os
import duckdb
from loguru import logger
from ingestion.src.utils.config import settings


def export_precios_json(output_path: str = "frontend/data/precios.json") -> None:
    logger.info("Exporting mart_precios_calculadora to JSON...")

    conn = duckdb.connect(settings.duckdb_path)

    df = conn.execute("""
        SELECT
            nivel,
            codigo,
            name_lugar,
            cod_prov,
            name_prov,
            clase_finca_urbana_id,
            clase_finca_urbana_desc,
            precio_m2,
            snapshot_date::varchar as snapshot_date
        FROM main.mart_precios_calculadora
        WHERE tipo_construccion_id = 99
        ORDER BY nivel, codigo, clase_finca_urbana_id
    """).df()

    conn.close()

    output = {
        "codigo_postal": {},
        "municipio": {},
        "provincia": {},
        "snapshot_date": df["snapshot_date"].max()
    }

    for _, row in df.iterrows():
        nivel = row["nivel"]
        codigo = str(row["codigo"])
        clase = str(row["clase_finca_urbana_id"])
        precio = row["precio_m2"]

        if codigo not in output[nivel]:
            output[nivel][codigo] = {}

        output[nivel][codigo][clase] = round(precio, 2)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(output, f, ensure_ascii=False)

    logger.info(f"Exported {len(df)} records to {output_path}")
    logger.info(f"  - codigo_postal: {len(output['codigo_postal'])} entries")
    logger.info(f"  - municipio: {len(output['municipio'])} entries")
    logger.info(f"  - provincia: {len(output['provincia'])} entries")


if __name__ == "__main__":
    export_precios_json()