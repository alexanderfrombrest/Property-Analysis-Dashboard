{{
    config(materialized="table")
}}

with otodom_property_recent as (
    select *,
        'otodom_property_recent' as service_type
    from {{ ref("stg_property_data_daily") }}
)

select
    otodom_property_recent.id,
    min(otodom_property_recent.download_date) as loaded_date,
    min(date(otodom_property_recent.added_date)) as added_date,
    max(date(otodom_property_recent.update_date)) as latest_update_date,
    avg(otodom_property_recent.price) as price,
    avg(otodom_property_recent.area) as area,
    avg(otodom_property_recent.price_per_m2) as price_per_m2,
    max(otodom_property_recent.building_year) as building_year,
    max(otodom_property_recent.heating) as heating,
    max(otodom_property_recent.form_of_ownership) as form_of_ownership,
    max(otodom_property_recent.condition) as condition,
    max(otodom_property_recent.arrangements) as arrangements,
    max(otodom_property_recent.elevator) as elevator_available,
    max(otodom_property_recent.voivodeship) as voivodeship,
    max(otodom_property_recent.city) as city,
    max(otodom_property_recent.district) as district,
    max(otodom_property_recent.subdistrict) as subdistrict,
    max(otodom_property_recent.link) as link

from otodom_property_recent
where
    id > 0
    and price_per_m2 > 0
    and price_per_m2 < 100000
    and area > 10
group by otodom_property_recent.id
