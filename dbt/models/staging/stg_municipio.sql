with source as (
    select * from read_parquet(
        '/workspaces/notariado-inmobiliario/data/raw/municipio/*/data.parquet'
    )
),

renamed as (
    select
        -- ids
        objectid,
        cod_ccaa,
        name_ccaa,
        cod_prov,
        name_prov,
        cod_muni,
        name_muni,
        mun_id_new,

        -- categorías
        tipo_construccion_id,
        clase_finca_urbana_id,
        es_estimado,

        -- métricas
        precio_m2,
        precio_medio,
        superficie_media,
        total_informados,
        total,

        -- metadata
        snapshot_date::date as snapshot_date

    from source
)

select * from renamed