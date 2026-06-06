import time
from loguru import logger
from ingestion.src.extractors.arcgis_client import ArcGISClient
from ingestion.src.utils.config import settings

TIPO_CONSTRUCCION = [7, 9, 99]
CLASE_FINCA = [14, 15, 99]


def fetch_all_records(layer: str) -> list[dict]:
    client = ArcGISClient()
    all_records = []

    try:
        for tipo in TIPO_CONSTRUCCION:
            for clase in CLASE_FINCA:
                offset = 0

                while True:
                    response = client.fetch_layer(
                        layer=layer,
                        tipo_construccion_id=tipo,
                        clase_finca_urbana_id=clase,
                        offset=offset,
                    )

                    features = response.get("features", [])
                    if not features:
                        break

                    all_records.extend([f["attributes"] for f in features])
                    logger.info(f"  → {len(all_records)} records so far")

                    if not response.get("exceededTransferLimit"):
                        break

                    offset += 2000
                    time.sleep(settings.request_delay_seconds)

    finally:
        client.close()

    return all_records