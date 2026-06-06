import os
import pyarrow as pa
import pyarrow.parquet as pq
from loguru import logger
from ingestion.src.utils.config import settings


def save_to_parquet(records: list, layer: str, snapshot_date: str) -> str:
    # Converting the Pydantic models to dicts
    data = [r.model_dump() for r in records]

    # Building the partiton rute by layer and date
    output_dir = os.path.join(settings.data_dir, "raw", layer, snapshot_date)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "data.parquet")

    # Parquet
    table = pa.Table.from_pylist(data)
    pq.write_table(table, output_path)

    logger.info(f"Saved {len(data)} records to {output_path}")
    return output_path