import json

def read_products(data):
    print(f"Trying to open the file at: {data}")
    with open(data, 'r') as file:
        products = json.load(file)

    first_product = products[0]
    columns = list(first_product['other_data'].keys())
    values = list(first_product['other_data'].values())

    return products, columns, values