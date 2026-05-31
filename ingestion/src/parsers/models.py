from pydantic import BaseModel


class MunicipioRecord(BaseModel):
    objectid: int
    name_ccaa: str | None
    cod_ccaa: str | None
    name_prov: str | None
    cod_prov: str | None
    name_muni: str | None
    cod_muni: str | None
    es_estimado: int | None
    precio_m2: float | None
    precio_medio: float | None
    superficie_media: float | None
    total_informados: int | None
    total: int | None
    tipo_construccion_id: int | None
    clase_finca_urbana_id: int | None