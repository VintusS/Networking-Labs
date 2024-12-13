import json
import sqlite3

def create_products(cursor, product):

    cursor.execute('''
    INSERT INTO product (href, img, name, converted_price, current_currency)
    VALUES (?, ?, ?, ?, ?)
    ''', (product['href'], product['img'], product['name'], product['converted_price'], product['current_currency']))

    product_id = cursor.lastrowid
    keys = list(product['other_data'].keys())
    values = list(product['other_data'].values())
    columns = ', '.join([f'"{column}"' for column in keys])
    placeholders = ', '.join(['?'] * (len(keys) + 1))

    values_list = [product_id] + values

    cursor.execute(f'''
    INSERT INTO other_data ("product_id", {columns})
    VALUES ({placeholders})
    ''', values_list)

    print("Product inserted successfully")