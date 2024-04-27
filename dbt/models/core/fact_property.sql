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
    otodom_property.link as id,
    MIN(DATE(otodom_property.added_date)) as added_date,
    MAX(DATE(otodom_property.update_date)) as latest_update_date,
    MIN(otodom_property.price) as initial_price, 
    MAX(otodom_property.price) as latest_price,
    MAX(otodom_property.price)- MIN(otodom_property.price) as price_change,
    AVG(otodom_property.area) as area,
    AVG(otodom_property.price_per_m2) as average_price_per_m2,
    MAX(otodom_property.price_per_m2) as max_price_per_m2,
    MAX(heating) as heating,
    MAX(form_of_ownership) as form_of_ownership,
    MAX(condition) as condition,
    MAX(arrangements) as arrangements,
    MAX(elevator) as elevator_available
    

from otodom_property
where 
    id > 0 AND
    price_per_m2 > 0 AND    
    price_per_m2 < 30000 AND
    condition <> "0" AND condition <> "do remontu" AND
    form_of_ownership <> "0"
group by otodom_property.link
order by condition asc

