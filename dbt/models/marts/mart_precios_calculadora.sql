with precios as (
    select * from {{ ref('int_precios_enriquecidos') }}
),

-- Precio más reciente por CP, tipo y clase
cp_latest as (
    select
        cp,
        tipo_construccion_id,
        tipo_construccion_desc,
        clase_finca_urbana_id,
        clase_finca_urbana_desc,
        precio_m2,
        precio_medio,
        superficie_media,
        total_informados,
        total,
        es_estimado,
        snapshot_date
    from precios
    where nivel = 'codigo_postal'
    qualify row_number() over (
        partition by cp, tipo_construccion_id, clase_finca_urbana_id
        order by snapshot_date desc
    ) = 1
),

-- Precio más reciente por municipio, tipo y clase (fallback nivel 2)
muni_latest as (
    select
        cod_muni,
        name_muni,
        cod_prov,
        name_prov,
        cod_ccaa,
        name_ccaa,
        tipo_construccion_id,
        tipo_construccion_desc,
        clase_finca_urbana_id,
        clase_finca_urbana_desc,
        precio_m2,
        precio_medio,
        superficie_media,
        total_informados,
        total,
        es_estimado,
        snapshot_date
    from precios
    where nivel = 'municipio'
    qualify row_number() over (
        partition by cod_muni, tipo_construccion_id, clase_finca_urbana_id
        order by snapshot_date desc
    ) = 1
),

-- Precio más reciente por provincia, tipo y clase (fallback nivel 3)
prov_latest as (
    select
        p.cod_prov,
        p.name_prov,
        p.cod_ccaa,
        p.name_ccaa,
        p.tipo_construccion_id,
        tc.tipo_construccion_desc,
        p.clase_finca_urbana_id,
        cf.clase_finca_urbana_desc,
        p.precio_m2,
        p.precio_medio,
        p.superficie_media,
        p.total_informados,
        p.total,
        p.es_estimado,
        p.snapshot_date
    from {{ ref('stg_provincia') }} p
    left join {{ ref('tipo_construccion') }} tc
        on p.tipo_construccion_id = tc.tipo_construccion_id
    left join {{ ref('clase_finca_urbana') }} cf
        on p.clase_finca_urbana_id = cf.clase_finca_urbana_id
    qualify row_number() over (
        partition by p.cod_prov, p.tipo_construccion_id, p.clase_finca_urbana_id
        order by p.snapshot_date desc
    ) = 1
)

select
    'codigo_postal'         as nivel,
    cp                      as codigo,
    null                    as name_lugar,
    null                    as cod_prov,
    null                    as name_prov,
    null                    as cod_ccaa,
    null                    as name_ccaa,
    tipo_construccion_id,
    tipo_construccion_desc,
    clase_finca_urbana_id,
    clase_finca_urbana_desc,
    precio_m2,
    precio_medio,
    superficie_media,
    total_informados,
    total,
    es_estimado,
    snapshot_date
from cp_latest

union all

select
    'municipio'             as nivel,
    cod_muni                as codigo,
    name_muni               as name_lugar,
    cod_prov,
    name_prov,
    cod_ccaa,
    name_ccaa,
    tipo_construccion_id,
    tipo_construccion_desc,
    clase_finca_urbana_id,
    clase_finca_urbana_desc,
    precio_m2,
    precio_medio,
    superficie_media,
    total_informados,
    total,
    es_estimado,
    snapshot_date
from muni_latest

union all

select
    'provincia'             as nivel,
    p.cod_prov              as codigo,
    p.name_prov             as name_lugar,
    null                    as cod_prov,
    p.name_prov,
    p.cod_ccaa,
    p.name_ccaa,
    p.tipo_construccion_id,
    p.tipo_construccion_desc,
    p.clase_finca_urbana_id,
    p.clase_finca_urbana_desc,
    p.precio_m2,
    p.precio_medio,
    p.superficie_media,
    p.total_informados,
    p.total,
    p.es_estimado,
    p.snapshot_date
from prov_latest p