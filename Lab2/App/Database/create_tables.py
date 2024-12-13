import sqlite3

def create_table_product(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        href TEXT NOT NULL,
        img TEXT NOT NULL,
        name TEXT NOT NULL,
        converted_price REAL NOT NULL,
        current_currency TEXT NOT NULL
    )
    ''')
    print("Table product created successfully")

def create_table_other_data(cursor, columns, values):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS other_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
    '''
    
    i=0
    for column in columns:
        if isinstance(values[i], (int, float)):
            create_table_sql += f"\"{column}\" INTEGER, "
        else:
            create_table_sql += f"\"{column}\" TEXT, "
        i += 1

    create_table_sql += 'FOREIGN KEY(product_id) REFERENCES product(id))'
    
    cursor.execute(create_table_sql)
    print("Table other_data created successfully")