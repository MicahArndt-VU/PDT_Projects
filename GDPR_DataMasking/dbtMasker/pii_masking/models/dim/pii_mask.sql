select "user_id",
        {{ mask_name('"name"') }} as name_masked,
        {{ mask_email('"email"') }} as email_hashed,
        {{ mask_phone('"phone_number"') }} as phone_masked,
        {{ mask_address('"address"') }} as address_masked,
        "transaction_id",
        "transaction_date",
        "product_name",
        "product_category",
        "quantity_purchased",
        "unit_price",
        "payment_method",
        "order_status" from {{ source('snowflake_source','fake_data') }}