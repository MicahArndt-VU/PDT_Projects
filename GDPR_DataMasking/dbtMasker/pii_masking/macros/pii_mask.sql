{% macro mask_name(name_col) %}
  initcap(split_part({{ name_col }}, ' ', 1)) || ' X.'
{% endmacro %}

{% macro mask_email(email_col) %}
  sha2({{ email_col }}, 256)  -- Hashing email for anonymization
{% endmacro %}

{% macro mask_phone(phone_col) %}
  regexp_replace({{ phone_col }}, '\\d', 'X') -- Replace digits with 'X'
{% endmacro %}

{% macro mask_address(address_col) %}
  'REDACTED'  -- Fully masking the address
{% endmacro %}