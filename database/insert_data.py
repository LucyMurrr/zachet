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

insert_materials_type = '''
INSERT INTO materials_types (type_name) VALUES 
('Гранулы'),
('Краски'),
('Нитки');
'''

insert_units = '''
INSERT INTO units (unit_type) VALUES 
('л'),
('м'),
('г'),
('кг');
'''

insert_suppliers_type = '''
INSERT INTO suppliers_types (supplier_type) VALUES 
('МКК'),
('ОАО'),
('ООО'),
('ЗАО'),
('МФО'),
('ПАО');
'''

cur.execute(insert_materials_type)
cur.execute(insert_units)
cur.execute(insert_suppliers_type)

conn.commit()

cur.close()
conn.close()