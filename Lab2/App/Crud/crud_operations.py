import json

def get_product(cursor, product_id, columns):
    cursor.execute('SELECT * FROM product WHERE id = ?', (product_id,))
    product_row = cursor.fetchone()
    if product_row is None:
        return None

    product_data = {
        "href": product_row[1],
        "img": product_row[2],
        "name": product_row[3],
        "converted_price": product_row[4],
        "current_currency": product_row[5]
    }

    cursor.execute('SELECT * FROM other_data WHERE product_id = ?', (product_id,))
    other_data_rows = cursor.fetchall()
    product_data['other_data'] = {}

    i=2
    for column in columns:
        product_data['other_data'][column] = other_data_rows[0][i]
        i+=1

    return product_data

def get_products_with_pagination(cursor, columns, offset, limit):
    cursor.execute('SELECT COUNT(*) FROM product')
    total_count = cursor.fetchone()[0]

    cursor.execute('SELECT * FROM product LIMIT ? OFFSET ?', (limit, offset))
    product_rows = cursor.fetchall()

    product_list = []
    for product_row in product_rows:
        product_id = product_row[0]
        product_data = {
            "href": product_row[1],
            "img": product_row[2],
            "name": product_row[3],
            "converted_price": product_row[4],
            "current_currency": product_row[5]
        }

        cursor.execute('SELECT * FROM other_data WHERE product_id = ?', (product_id,))
        other_data_rows = cursor.fetchall()

        product_data['other_data'] = {}
        i = 2
        for column in columns:
            product_data['other_data'][column] = other_data_rows[0][i] if other_data_rows else None
            i += 1

        product_list.append(product_data)

    return product_list, total_count 

def create_product(cursor, product):
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

    print("Product inserted successfully", product_id)  
    return product_id

def update_product_data(cursor, product_id, data):
    cursor.execute('''
    UPDATE product
    SET href = ?, img = ?, name = ?, converted_price = ?, current_currency = ?
    WHERE id = ?
    ''', (data['href'], data['img'], data['name'], data['converted_price'], data['current_currency'], product_id))

    for key, value in data['other_data'].items():
        cursor.execute(f'''
        UPDATE other_data
        SET "{key}" = ?
        WHERE product_id = ?
        ''', (value, product_id))

    print("Product updated successfully", product_id)

def delete_product_data(cursor, product_id):
    cursor.execute('DELETE FROM other_data WHERE product_id = ?', (product_id,))
    cursor.execute('DELETE FROM product WHERE id = ?', (product_id,))

    print("Product deleted successfully", product_id)