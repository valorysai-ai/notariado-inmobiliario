with municipio as (
    select * from {{ ref('stg_municipio') }}
),

codigo_postal as (
    select * from {{ ref('stg_codigo_postal') }}
),

tipo_construccion as (
    select * from {{ ref('tipo_construccion') }}
),

clase_finca as (
    select * from {{ ref('clase_finca_urbana') }}
),

municipio_enriquecido as (
    select
        m.snapshot_date,
        m.cod_ccaa,
        m.name_ccaa,
        m.cod_prov,
        m.name_prov,
        m.cod_muni,
        m.name_muni,
        m.tipo_construccion_id,
        tc.tipo_construccion_desc,
        m.clase_finca_urbana_id,
        cf.clase_finca_urbana_desc,
        m.precio_m2,
        m.precio_medio,
        m.superficie_media,
        m.total_informados,
        m.total,
        m.es_estimado
    from municipio m
    left join tipo_construccion tc
        on m.tipo_construccion_id = tc.tipo_construccion_id
    left join clase_finca cf
        on m.clase_finca_urbana_id = cf.clase_finca_urbana_id
),

cp_enriquecido as (
    select
        cp.snapshot_date,
        cp.cp,
        cp.tipo_construccion_id,
        tc.tipo_construccion_desc,
        cp.clase_finca_urbana_id,
        cf.clase_finca_urbana_desc,
        cp.precio_m2,
        cp.precio_medio,
        cp.superficie_media,
        cp.total_informados,
        cp.total,
        cp.es_estimado
    from codigo_postal cp
    left join tipo_construccion tc
        on cp.tipo_construccion_id = tc.tipo_construccion_id
    left join clase_finca cf
        on cp.clase_finca_urbana_id = cf.clase_finca_urbana_id
)

select
    'codigo_postal' as nivel,
    cp.snapshot_date,
    cp.cp,
    null as cod_muni,
    null as name_muni,
    null as cod_prov,
    null as name_prov,
    null as cod_ccaa,
    null as name_ccaa,
    cp.tipo_construccion_id,
    cp.tipo_construccion_desc,
    cp.clase_finca_urbana_id,
    cp.clase_finca_urbana_desc,
    cp.precio_m2,
    cp.precio_medio,
    cp.superficie_media,
    cp.total_informados,
    cp.total,
    cp.es_estimado
from cp_enriquecido cp

union all

select
    'municipio' as nivel,
    m.snapshot_date,
    null as cp,
    m.cod_muni,
    m.name_muni,
    m.cod_prov,
    m.name_prov,
    m.cod_ccaa,
    m.name_ccaa,
    m.tipo_construccion_id,
    m.tipo_construccion_desc,
    m.clase_finca_urbana_id,
    m.clase_finca_urbana_desc,
    m.precio_m2,
    m.precio_medio,
    m.superficie_media,
    m.total_informados,
    m.total,
    m.es_estimado
from municipio_enriquecido m