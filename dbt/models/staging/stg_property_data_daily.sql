with

    source as (select * from {{ source("staging", "property_data_daily") }}),

    renamed1 as (

        select
            `current_date` as download_date,
            `current_time` as download_time,
            id,
            added_date,
            update_date,
            price,
            area,
            rooms,
            floor,
            rent,
            form_of_ownership,
            condition,
            arrangements,
            heating,
            market,
            advertiser_type,
            building_year,
            material1,
            elevator,
            material2,
            link,
            voivodeship,
            city,
            district,
            subdistrict,
            price_per_m2

        from source

    )

select *
from renamed1
order by id desc
