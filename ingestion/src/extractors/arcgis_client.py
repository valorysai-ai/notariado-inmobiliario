import httpx
from loguru import logger
from ingestion.src.utils.config import settings


LAYERS = {
    "nacional": 0,
    "ccaa": 1,
    "provincia": 2,
    "municipio": 3,
    "codigo_postal": 4,
}


class ArcGISClient:

    def __init__(self):
        self.base_url = settings.arcgis_base_url
        self.client = httpx.Client(timeout=30)

    def fetch_layer(
        self,
        layer: str,
        tipo_construccion_id: int,
        clase_finca_urbana_id: int,
        offset: int = 0,
    ) -> dict:
        layer_id = LAYERS[layer]
        url = f"{self.base_url}/{layer_id}/query"

        params = {
            "f": "json",
            "where": f"(tipo_construccion_id = {tipo_construccion_id}) AND (clase_finca_urbana_id = {clase_finca_urbana_id})",
            "outFields": "*",
            "resultRecordCount": 2000,
            "resultOffset": offset,
            "orderByFields": "OBJECTID ASC",
        }

        logger.info(f"Fetching layer={layer} tipo={tipo_construccion_id} clase={clase_finca_urbana_id} offset={offset}")
        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()