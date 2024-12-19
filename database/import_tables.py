import psycopg2
import csv
from datetime import datetime
from config import db_config

def import_data_from_csv(file_path, table_name):
    conn = psycopg2.connect(
        dbname=db_config['dbname'],
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host'],
        port=db_config['port']
    )

    cur = conn.cursor()

    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)

        for row in reader:
            if not row:
                continue
            
            if table_name == 'materials':
                if len(row) != 8:
                    print(f"Неверное количество столбцов в строке: {row}")
                    continue

                material_id = int(row[0])
                cur.execute('SELECT COUNT(*) FROM materials WHERE material_id = %s', (material_id,))
                exists = cur.fetchone()[0]

                if exists > 0:
                    cur.execute('UPDATE materials SET type_id = %s, image = %s, price = %s, stock_quantity = %s, min_quantity = %s, package_quantity = %s, unit_id = %s WHERE material_id = %s',
                                (row[1], row[2], row[3], row[4], row[5], row[6], row[7], material_id))
                    print(f"Обновлена запись с material_id {material_id}.")
                else:
                    cur.execute('SELECT COUNT(*) FROM materials_names WHERE material_id = %s', (material_id,))
                    exists = cur.fetchone()[0]
                    if exists == 0:
                        print(f"material_id {material_id} не существует в materials_names.")
                        continue

                    cur.execute('INSERT INTO materials (material_id, type_id, image, price, stock_quantity, min_quantity, package_quantity, unit_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', row)
                    print(f"Добавлена новая запись с material_id {material_id}.")

            elif table_name == 'materials_names':
                if len(row) != 1:
                    print(f"Неверное количество столбцов в строке: {row}")
                    continue
                
                material_name = row[0]
                cur.execute('INSERT INTO materials_names (material_name) VALUES (%s)', (material_name,))
                print(f"Добавлена новая запись с material_name: {material_name}.")

            elif table_name == 'suppliers_names':
                if len(row) != 1:
                    print(f"Неверное количество столбцов в строке: {row}")
                    continue
                
                supplier_name = row[0]
                cur.execute('INSERT INTO suppliers_names (supplier_name) VALUES (%s)', (supplier_name,))
                print(f"Добавлена новая запись с supplier_name: {supplier_name}.")

            elif table_name == 'suppliers':
                if len(row) != 5:
                    print(f"Неверное количество столбцов в строке: {row}")
                    continue

                supplier_id = int(row[0])
                start_date = datetime.strptime(row[4], '%d.%m.%Y').date()
                cur.execute('SELECT COUNT(*) FROM suppliers WHERE supplier_id = %s', (supplier_id,))
                exists = cur.fetchone()[0]

                if exists > 0:
                    cur.execute('UPDATE suppliers SET supplier_type_id = %s, inn = %s, quality_rating = %s, start_date = %s WHERE supplier_id = %s',
                    (row[1], row[2], row[3], start_date, supplier_id))
                    print(f"Обновлена запись с supplier_id {supplier_id} в suppliers.")
                else:
                    cur.execute('INSERT INTO suppliers (supplier_id, supplier_type_id, inn, quality_rating, start_date) VALUES (%s, %s, %s, %s, %s)', (supplier_id, row[1], row[2], row[3], start_date))
                    print(f"Добавлена новая запись с supplier_id {supplier_id} в suppliers.")

            elif table_name == 'potential_suppliers':
                if len(row) != 2:
                    print(f"Неверное количество столбцов в строке: {row}")
                    continue
                
                cur.execute('INSERT INTO potential_suppliers (material_id, potential_supplier_id) VALUES (%s, %s) ON CONFLICT DO NOTHING', row)

    conn.commit()
    cur.close()
    conn.close()

import_data_from_csv('csv/materials.csv', 'materials')
import_data_from_csv('csv/materials_names.csv', 'materials_names')
import_data_from_csv('csv/suppliers_names.csv', 'suppliers_names')
import_data_from_csv('csv/suppliers.csv', 'suppliers')
import_data_from_csv('csv/potential_suppliers.csv', 'potential_suppliers')