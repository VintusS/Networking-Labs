import sys
import sqlite3
import json
import os
from create_tables import create_table_product, create_table_other_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Process.read import read_products
from Crud.crud_operations import create_product

def main(cursor, columns, values, products):
    #free_database(cursor)
    create_table_product(cursor)
    create_table_other_data(cursor, columns, values)
    # for product in products:
    #     create_product(cursor, product)
    print("Database Processing Done")

database = '/Users/dragomirmindrescu/Downloads/PR-main/Lab2/App/Database/products.db'
data = '/Users/dragomirmindrescu/Downloads/PR-main/Lab2/App/Database/products.json'

products, columns, values = read_products(data)

conn = sqlite3.connect(database)
cursor = conn.cursor()

main(cursor, columns, values, products)
conn.commit()
conn.close()
