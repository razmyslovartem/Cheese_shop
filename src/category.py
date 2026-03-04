from typing import Dict
from typing import List
from typing import Optional


class Product:
    """Класс для товаров"""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для получения цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: Dict) -> "Product":
        """Класс-метод для создания продукта из словаря"""
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )


class Category:
    """Класс для категорий товаров"""

    category_count: int = 0  # счетчик категорий
    product_count: int = 0  # счетчик товаров

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        self.name = name
        self.description = description
        self.__products: List[Product] = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    @property
    def products(self) -> str:
        """
        Геттер для получения списка товаров в отформатированном виде.
        Возвращает строку с информацией о каждом товаре в формате:
        "Название продукта, 80 руб. Остаток: 15 шт."
        """
        if not self.__products:
            return "В категории нет товаров"

        result = []
        for product in self.__products:
            price = product.price
            # Для красивого вывода убираем .0 если это целое число
            price_str = str(int(price)) if price.is_integer() else str(price)
            product_str = f"{product.name}, {price_str} руб. Остаток: {product.quantity} шт."
            result.append(product_str)

        return "\n".join(result)

    def add_product(self, new_product: Product) -> None:
        self.__products.append(new_product)

        Category.product_count += 1
