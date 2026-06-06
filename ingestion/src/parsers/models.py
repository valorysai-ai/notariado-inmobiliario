from pydantic import BaseModel, Field


class BaseRecord(BaseModel):
    model_config = {"populate_by_name": True}
    
    objectid: int = Field(alias="OBJECTID")
    es_estimado: int | None
    precio_m2: float | None
    precio_medio: float | None
    superficie_media: float | None
    total_informados: int | None
    total: int | None
    tipo_construccion_id: int | None
    clase_finca_urbana_id: int | None
    snapshot_date: str

class NacionalRecord(BaseRecord):
    nac_id: int | None


class CCAARecord(BaseRecord):
    name_ccaa: str | None
    cod_ccaa: str | None
    ccaa_id_new: int | None


class ProvinciaRecord(BaseRecord):
    name_ccaa: str | None
    cod_ccaa: str | None
    name_prov: str | None
    cod_prov: str | None
    prv_id_new: int | None


class MunicipioRecord(BaseRecord):
    name_ccaa: str | None
    cod_ccaa: str | None
    name_prov: str | None
    cod_prov: str | None
    name_muni: str | None
    cod_muni: str | None
    mun_id_new: int | None


class CodigoPostalRecord(BaseRecord):
    cp: str | None
    cp_id_new: int | None