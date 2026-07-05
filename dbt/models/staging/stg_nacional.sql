with source as (
    select * from read_parquet(
        'data/raw/nacional/*/data.parquet'
    )
),

renamed as (
    select
        objectid,
        nac_id,
        tipo_construccion_id,
        clase_finca_urbana_id,
        es_estimado,
        precio_m2,
        precio_medio,
        superficie_media,
        total_informados,
        total,
        snapshot_date::date as snapshot_date
    from source
)

select * from renamed