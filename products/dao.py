import os
import sqlite3
from typing import List, Dict, Union

def connect(path: str = 'products.db') -> sqlite3.Connection:
    exists = os.path.exists(path)
    conn = sqlite3.connect(path)
    if not exists:
        create_tables(conn)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(conn: sqlite3.Connection):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            cost REAL NOT NULL,
            qty INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    
    # Seed products if table is empty
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM products')
    if cursor.fetchone()['count'] == 0:
        seed_products = [
    ('Backpack', 'A durable and stylish backpack for daily use.', 800.0, 10),
    ('Wireless Mouse', 'A sleek and ergonomic wireless mouse with a long battery life.', 800.0, 20),
    ('Bluetooth Speaker', 'A portable Bluetooth speaker with high-quality sound and deep bass.', 3000.0, 30),
    ('Laptop Stand', 'An adjustable laptop stand for better posture and cooling.', 250.0, 15),
    ('Notebook', 'A premium notebook with thick, high-quality paper.', 50.0, 50),
    ('Smartphone Case', 'A durable and stylish case for protecting your smartphone.', 150.0, 25),
    ('Power Bank', 'A high-capacity power bank with fast charging support.', 900.0, 20),
    ('Headphones', 'Over-ear headphones with noise cancellation and deep bass.', 5000.0, 10),
    ('Gaming Keyboard', 'A mechanical gaming keyboard with RGB lighting.', 3000.0, 10),
    ('USB-C Hub', 'A multi-port USB-C hub for all your connectivity needs.', 400.0, 25),
    ('Fitness Tracker', 'A sleek fitness tracker with heart rate monitoring.', 1000.0, 20),
    ('Travel Mug', 'An insulated travel mug that keeps your drinks hot or cold.', 500.0, 30),
    ('Desk Organizer', 'A compact desk organizer for keeping your workspace tidy.', 1200.0, 40),
    ('External Hard Drive', 'A portable external hard drive with 1TB of storage.', 800.0, 15),
    ('Wireless Charger', 'A fast wireless charger compatible with most devices.', 2500.0, 30),
    ('Digital Camera', 'A compact digital camera with 4K video recording.', 20000.0, 5),
    ('Electric Kettle', 'A fast-boiling electric kettle with auto shut-off.', 3000.0, 20),
    ('Smart Watch', 'A stylish smartwatch with fitness and notification features.', 12000.0, 10),
    ('LED Desk Lamp', 'A modern LED desk lamp with adjustable brightness.', 2000.0, 35),
    ('Portable Projector', 'A mini portable projector with HD resolution.', 15000.0, 8)
]
        conn.executemany(
            'INSERT INTO products (name, description, cost, qty) VALUES (?, ?, ?, ?)', 
            seed_products
        )
        conn.commit()

def list_products() -> List[sqlite3.Row]:
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        return cursor.fetchall()

def add_product(product: Dict[str, Union[str, float, int]]):
    with connect() as conn:
        conn.execute(
            'INSERT INTO products (name, description, cost, qty) VALUES (?, ?, ?, ?)',
            (product['name'], product['description'], product['cost'], product['qty'])
        )

def get_product(product_id: int) -> sqlite3.Row:
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        return cursor.fetchone()

def update_qty(product_id: int, qty: int):
    with connect() as conn:
        conn.execute('UPDATE products SET qty = ? WHERE id = ?', (qty, product_id))

def delete_product(product_id: int):
    with connect() as conn:
        conn.execute('DELETE FROM products WHERE id = ?', (product_id,))

def update_product(product_id: int, product: Dict[str, Union[str, float, int]]):
    with connect() as conn:
        conn.execute(
            'UPDATE products SET name = ?, description = ?, cost = ?, qty = ? WHERE id = ?',
            (product['name'], product['description'], product['cost'], product['qty'], product_id)
        )
