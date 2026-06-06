from datetime import date
from loguru import logger
from ingestion.src.parsers.models import (
    NacionalRecord,
    CCAARecord,
    ProvinciaRecord,
    MunicipioRecord,
    CodigoPostalRecord,
)

LAYER_MODELS = {
    "nacional": NacionalRecord,
    "ccaa": CCAARecord,
    "provincia": ProvinciaRecord,
    "municipio": MunicipioRecord,
    "codigo_postal": CodigoPostalRecord,
}


def parse_records(layer: str, raw_records: list[dict]) -> list:
    model = LAYER_MODELS[layer]
    snapshot = str(date.today())
    parsed = []

    for record in raw_records:
        record["snapshot_date"] = snapshot
        try:
            parsed.append(model(**record))
        except Exception as e:
            logger.warning(f"Skipping invalid record {record.get('OBJECTID')}: {e}")

    logger.info(f"Parsed {len(parsed)}/{len(raw_records)} records for layer={layer}")
    return parsed