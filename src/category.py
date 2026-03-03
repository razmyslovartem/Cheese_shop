from typing import List
from typing import Optional


class Product:
    """Класс для товаров"""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для категорий товаров"""

    category_count: int = 0  # счетчик категорий
    product_count: int = 0  # счетчик товаров

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        self.name = name
        self.description = description
        self.products: List[Product] = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.products)
