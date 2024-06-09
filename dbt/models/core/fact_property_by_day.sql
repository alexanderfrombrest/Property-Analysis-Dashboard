{{ config(materialized="table") }}

with
    otodom_property as (
        select *, 'otodom' as service_type from {{ ref("stg_property_data") }}
    )

select
    otodom_property.id,
    date(otodom_property.download_date) as download_date,
    max(date(otodom_property.update_date)) as latest_update_date,
    min(otodom_property.price) as initial_price,
    max(otodom_property.price) as latest_price,
    max(otodom_property.price) - min(otodom_property.price) as price_change,
    avg(otodom_property.area) as area,
    max(otodom_property.building_year) as building_year,
    avg(otodom_property.price_per_m2) as average_price_per_m2,
    max(otodom_property.price_per_m2) as max_price_per_m2,
    max(otodom_property.heating) as heating,
    max(otodom_property.form_of_ownership) as form_of_ownership,
    max(otodom_property.condition) as condition,
    max(otodom_property.arrangements) as arrangements,
    max(otodom_property.elevator) as elevator_available,
    max(otodom_property.voivodeship) as voivodeship,
    max(otodom_property.city) as city,
    max(otodom_property.district) as district,
    max(otodom_property.subdistrict) as subdistrict,
    max(otodom_property.link) as link

from otodom_property
where id > 0 and price_per_m2 > 0 and price_per_m2 < 50000 and area > 10
group by otodom_property.id, otodom_property.download_date
