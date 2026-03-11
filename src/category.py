from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Optional


class ReprMixin:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Конструктор миксина, который выводит информацию о создаваемом объекте"""
        # Вызываем __init__ следующего класса в MRO
        super().__init__(*args, **kwargs)
        # Выводим информацию о созданном объекте
        print(f"Создан объект: {self.__repr__()}")

    def __repr__(self) -> str:
        """Магический метод для представления объекта"""
        # Получаем все атрибуты объекта, кроме служебных
        attributes = []
        for key, value in self.__dict__.items():
            # Пропускаем приватные атрибуты (начинающиеся с _)
            if not key.startswith("_"):
                attributes.append(f"{key}={value!r}")

        # Формируем строку вида: ClassName(attr1=value1, attr2=value2, ...)
        return f"{self.__class__.__name__}({', '.join(attributes)})"


class BaseProduct(ABC):
    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Абстрактный метод инициализации"""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Абстрактный метод для строкового представления"""
        pass

    @abstractmethod
    def __add__(self, other: "BaseProduct") -> float:
        """Абстрактный метод для сложения продуктов"""
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        """Абстрактный геттер для цены"""
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float) -> None:
        """Абстрактный сеттер для цены"""
        pass


class Product(ReprMixin, BaseProduct):
    """Класс для товаров"""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        # Вызываем __init__ родительских классов
        super().__init__(name, description, price, quantity)

    def __str__(self) -> str:
        """Строковое представление продукта"""
        price_str = str(int(self.__price)) if self.__price.is_integer() else str(self.__price)
        return f"{self.name}, {price_str} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: BaseProduct) -> float:
        """
        Сложение двух продуктов для получения общей стоимости на складе.
        Можно складывать только объекты одного класса (проверка через type()).
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")

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


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        super().__init__(name, description, price, quantity)

    def __repr__(self) -> str:
        """Переопределяем __repr__ для Smartphone с учётом всех атрибутов"""
        return (
            f"Smartphone(name={self.name!r}, description={self.description!r}, "
            f"price={self.price!r}, quantity={self.quantity!r}, "
            f"efficiency={self.efficiency!r}, model={self.model!r}, "
            f"memory={self.memory!r}, color={self.color!r})"
        )


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        self.country = country
        self.germination_period = germination_period
        self.color = color
        super().__init__(name, description, price, quantity)

    def __repr__(self) -> str:
        """Переопределяем __repr__ для LawnGrass с учётом всех атрибутов"""
        return (
            f"LawnGrass(name={self.name!r}, description={self.description!r}, "
            f"price={self.price!r}, quantity={self.quantity!r}, "
            f"country={self.country!r}, germination_period={self.germination_period!r}, "
            f"color={self.color!r})"
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
        """
        Добавляет продукт в категорию.
        Принимает только объекты класса Product или его наследников.
        """
        if not isinstance(new_product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")

        self.__products.append(new_product)

        Category.product_count += 1
