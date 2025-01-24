import json
import products
from cart import dao
from products import Product

class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @classmethod
    def load(cls, data: dict) -> 'Cart':
        return cls(data['id'], data['username'], data['contents'], data['cost'])

def get_cart(username: str) -> list[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []
    
    # Safely eval contents and get products
    items = []
    for cart_detail in cart_details:
        try:
            contents = eval(cart_detail['contents'])
            items.extend(products.get_product(item) for item in contents)
        except (SyntaxError, TypeError) as e:
            # Log error or handle gracefully
            print(f"Error processing cart contents: {e}")
    
    return items
    
def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)
