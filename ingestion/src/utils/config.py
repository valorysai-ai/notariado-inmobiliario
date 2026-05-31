from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API
    arcgis_base_url: str

    # Storage
    data_dir: str
    duckdb_path: str

    # Ingestion
    request_delay_seconds: int
    max_retries: int
    log_level: str

    class Config:
        env_file = ".env"


settings = Settings()