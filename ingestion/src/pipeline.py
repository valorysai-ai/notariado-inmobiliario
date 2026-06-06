from datetime import date
from loguru import logger
from ingestion.src.extractors.fetcher import fetch_all_records
from ingestion.src.parsers.parser import parse_records
from ingestion.src.storage.parquet_writer import save_to_parquet

LAYERS = ["nacional", "ccaa", "provincia", "municipio", "codigo_postal"]


def run_pipeline(layers: list[str] = LAYERS) -> None:
    snapshot_date = str(date.today())
    logger.info(f"Starting pipeline — snapshot_date={snapshot_date}")

    for layer in layers:
        logger.info(f"Processing layer: {layer}")

        raw_records = fetch_all_records(layer)
        parsed_records = parse_records(layer, raw_records)
        save_to_parquet(parsed_records, layer, snapshot_date)

        logger.info(f"Layer {layer} completed — {len(parsed_records)} records saved")

    logger.info("Pipeline completed successfully")