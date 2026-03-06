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

    def __str__(self) -> str:
        """Строковое представление продукта"""
        price_str = str(int(self.__price)) if self.__price.is_integer() else str(self.__price)
        return f"{self.name}, {price_str} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """
        Сложение двух продуктов для получения общей стоимости на складе.
        Возвращает сумму произведений цены на количество для двух продуктов.
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")
        return (self.__price * self.quantity) + (other.__price * other.quantity)

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

    def __str__(self) -> str:
        """
        Строковое представление категории.
        Считает общее количество товаров на складе (сумму quantity всех продуктов).
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов {total_quantity} шт."

    @property
    def products(self) -> str:
        """
        Геттер для получения списка товаров в отформатированном виде.
        Теперь использует __str__ каждого продукта.
        """
        if not self.__products:
            return "В категории нет товаров"

        # Используем __str__ каждого продукта
        return "\n".join(str(product) for product in self.__products)

    def add_product(self, new_product: Product) -> None:
        self.__products.append(new_product)

        Category.product_count += 1
