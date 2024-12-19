import psycopg2
from config import db_config

conn = psycopg2.connect(
    dbname=db_config['dbname'],
    user=db_config['user'],
    password=db_config['password'],
    host=db_config['host'],
    port=db_config['port']
)

cur = conn.cursor()

create_tables_sql = '''
CREATE TABLE IF NOT EXISTS materials_types (
    type_id BIGSERIAL PRIMARY KEY,
    type_name CHARACTER VARYING(100)
);

CREATE TABLE IF NOT EXISTS materials_names (
    material_id BIGSERIAL PRIMARY KEY,
    material_name CHARACTER VARYING(100)
);

CREATE TABLE IF NOT EXISTS units (
    unit_id BIGSERIAL PRIMARY KEY,
    unit_type CHARACTER VARYING(50)
);

CREATE TABLE IF NOT EXISTS suppliers_types (
    supplier_type_id BIGSERIAL PRIMARY KEY,
    supplier_type CHARACTER VARYING(100)
);

CREATE TABLE IF NOT EXISTS suppliers_names (
    supplier_id BIGSERIAL PRIMARY KEY,
    supplier_name CHARACTER VARYING(100)
);

CREATE TABLE IF NOT EXISTS materials (
    material_id BIGINT PRIMARY KEY REFERENCES materials_names(material_id),
    type_id BIGINT REFERENCES materials_types(type_id),
    image CHARACTER VARYING(100),
    price MONEY,
    stock_quantity BIGINT,
    min_quantity BIGINT,
    package_quantity BIGINT,
    unit_id BIGINT REFERENCES units(unit_id)
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id BIGINT PRIMARY KEY REFERENCES suppliers_names(supplier_id),
    supplier_type_id BIGINT REFERENCES suppliers_types(supplier_type_id),
    inn BIGINT,
    quality_rating BIGINT,
    start_date DATE
);

CREATE TABLE IF NOT EXISTS potential_suppliers (
    material_id BIGINT REFERENCES materials(material_id),
    potential_supplier_id BIGINT REFERENCES suppliers(supplier_id)
);
'''

cur.execute(create_tables_sql)
conn.commit()

cur.close()
conn.close()