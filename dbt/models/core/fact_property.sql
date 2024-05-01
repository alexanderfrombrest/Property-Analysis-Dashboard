{{

    config (
        materialized = 'table'
    )
}}

with otodom_property as (
    select *,
        'otodom' as service_type
    from {{ ref('stg_property_data')}}
) 

select
    otodom_property.id,
    MIN(DATE(otodom_property.added_date)) as added_date,
    MAX(DATE(otodom_property.update_date)) as latest_update_date,
    MIN(otodom_property.price) as initial_price, 
    MAX(otodom_property.price) as latest_price,
    MAX(otodom_property.price)- MIN(otodom_property.price) as price_change,
    AVG(otodom_property.area) as area,
    AVG(otodom_property.price_per_m2) as average_price_per_m2,
    MAX(otodom_property.price_per_m2) as max_price_per_m2,
    MAX(otodom_property.heating) as heating,
    MAX(otodom_property.form_of_ownership) as form_of_ownership,
    MAX(otodom_property.condition) as condition,
    MAX(otodom_property.arrangements) as arrangements,
    MAX(otodom_property.elevator) as elevator_available,
    MAX(otodom_property.voivodeship) as voivodeship,
    MAX(otodom_property.city) as city,
    MAX(otodom_property.district) as district,
    MAX(otodom_property.subdistrict) as subdistrict,
    MAX(otodom_property.link) as link
    

from otodom_property
where 
    id > 0 AND
    price_per_m2 > 0 AND    
    price_per_m2 < 50000 AND
    area > 10
group by otodom_property.id

