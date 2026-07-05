with source as (
    select * from read_parquet(
        '{{ var("project_root") }}/data/raw/provincia/*/data.parquet'
    )
),

renamed as (
    select
        objectid,
        cod_ccaa,
        name_ccaa,
        cod_prov,
        name_prov,
        prv_id_new,
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