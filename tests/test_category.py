from _pytest.capture import CaptureFixture
import pytest

from src.category import Category
from src.category import Product


@pytest.fixture()
def sample_product_1() -> Product:
    return Product("Iphone 17 Pro", "1TB, Cosmic Orange", 189000.0, 3)


@pytest.fixture()
def sample_product_2() -> Product:
    return Product("Samsung Galaxy S25", "512GB, Phantom Black", 150000.0, 5)


@pytest.fixture()
def sample_product_3() -> Product:
    return Product("Xiaomi Mi 14", "256GB, Green", 50000.0, 10)


@pytest.fixture()
def sample_category(sample_product_1: Product, sample_product_2: Product) -> Category:
    return Category("Тестовая категория товаров", "Тестовое описание товаров", [sample_product_1, sample_product_2])


def test_init_product(sample_product_1: Product, sample_product_2: Product, sample_product_3: Product) -> None:
    """Тест на корректность инициализации объектов класса Product"""
    assert sample_product_1.name == "Iphone 17 Pro"
    assert sample_product_1.description == "1TB, Cosmic Orange"
    assert sample_product_1.price == 189000.0
    assert sample_product_1.quantity == 3

    assert sample_product_2.name == "Samsung Galaxy S25"
    assert sample_product_2.description == "512GB, Phantom Black"
    assert sample_product_2.price == 150000.0
    assert sample_product_2.quantity == 5

    assert sample_product_3.name == "Xiaomi Mi 14"
    assert sample_product_3.description == "256GB, Green"
    assert sample_product_3.price == 50000.0
    assert sample_product_3.quantity == 10


def test_init_category(sample_category: Category, sample_product_1: Product, sample_product_2: Product) -> None:
    """Тест на корректность инициализации объектов класса Category"""
    assert sample_category.name == "Тестовая категория товаров"
    assert sample_category.description == "Тестовое описание товаров"
    # Используем getattr для доступа к приватному атрибуту (обход проверки mypy)
    products = getattr(sample_category, "_Category__products")
    assert len(products) == 2
    assert products[0] == sample_product_1
    assert products[1] == sample_product_2


def test_category_products_property(sample_category: Category) -> None:
    """Тест геттера products (должен возвращать строку с отформатированными товарами)"""
    products_str = sample_category.products
    expected = "Iphone 17 Pro, 189000 руб. Остаток: 3 шт.\nSamsung Galaxy S25, 150000 руб. Остаток: 5 шт."
    assert products_str == expected


def test_category_products_property_empty() -> None:
    """Тест геттера products для пустой категории"""
    category = Category("Пустая категория", "Описание")
    assert category.products == "В категории нет товаров"


def test_add_product(sample_category: Category, sample_product_3: Product) -> None:
    """Тест метода add_product"""
    initial_count = Category.product_count
    # Используем getattr для доступа к приватному атрибуту
    products = getattr(sample_category, "_Category__products")
    initial_len = len(products)

    sample_category.add_product(sample_product_3)

    # Снова используем getattr для получения обновленного списка
    updated_products = getattr(sample_category, "_Category__products")
    assert len(updated_products) == initial_len + 1
    assert updated_products[-1] == sample_product_3
    assert Category.product_count == initial_count + 1


def test_category_count() -> None:
    """Тест на подсчет количества категорий"""
    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0

    Category("Категория 1", "Описание 1")
    assert Category.category_count == 1

    Category("Категория 2", "Описание 2")
    assert Category.category_count == 2


def test_product_count(sample_product_1: Product, sample_product_2: Product, sample_product_3: Product) -> None:
    """Тест на подсчет количества товаров во всех категориях"""
    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0

    # Категория с 2 товарами
    Category("Категория с товарами", "Описание", [sample_product_1, sample_product_2])
    assert Category.product_count == 2

    # Категория с 1 товаром
    Category("Еще категория", "Описание", [sample_product_3])
    assert Category.product_count == 3  # 2 + 1 = 3

    # Пустая категория
    Category("Пустая категория", "Описание")
    assert Category.product_count == 3  # не изменилось


def test_product_new_classmethod() -> None:
    """Тест класс-метода new_product"""
    product_data = {"name": "Тестовый продукт", "description": "Тестовое описание", "price": 999.99, "quantity": 10}

    product = Product.new_product(product_data)

    assert product.name == "Тестовый продукт"
    assert product.description == "Тестовое описание"
    assert product.price == 999.99
    assert product.quantity == 10


def test_product_price_property() -> None:
    """Тест геттера и сеттера для цены продукта"""
    product = Product("Тест", "Описание", 100.0, 5)
    assert product.price == 100.0
    product.price = 150.0
    assert product.price == 150.0
    product.price = -50.0
    assert product.price == 150.0  # Цена не изменилась
    product.price = 0.0
    assert product.price == 150.0  # Цена не изменилась


def test_product_price_setter_with_negative(capsys: CaptureFixture) -> None:
    """Тест вывода сообщения при установке отрицательной цены"""
    product = Product("Тест", "Описание", 100.0, 5)

    product.price = -50.0
    captured = capsys.readouterr()
    assert captured.out.strip() == "Цена не должна быть нулевая или отрицательная"

    product.price = 0.0
    captured = capsys.readouterr()
    assert captured.out.strip() == "Цена не должна быть нулевая или отрицательная"


def test_products_formatting_with_integer_price() -> None:
    """Тест форматирования цены: целые числа должны выводиться без .0"""
    product = Product("Тест", "Описание", 100.0, 5)
    category = Category("Тест", "Описание", [product])

    # Проверяем, что цена выводится как "100", а не "100.0"
    assert "100 руб." in category.products
    assert "100.0 руб." not in category.products


def test_products_formatting_with_float_price() -> None:
    """Тест форматирования цены: дробные числа должны выводиться с точкой"""
    product = Product("Тест", "Описание", 99.99, 5)
    category = Category("Тест", "Описание", [product])

    # Проверяем, что цена выводится как "99.99"
    assert "99.99 руб." in category.products


# НОВЫЕ ТЕСТЫ ДЛЯ ЗАДАНИЯ 3 (ПРОДОЛЖЕНИЕ С ЗАДАНИЕМ 4)

def test_product_add_method_different_classes() -> None:
    """Тест __add__ с объектами разных классов (должно вызывать TypeError)"""
    # Создаем продукты разных классов
    class DifferentClass:
        pass

    product = Product("Тест", "Описание", 100.0, 5)
    not_a_product = DifferentClass()

    with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
        product + not_a_product  # type: ignore


def test_product_add_method_same_class_with_inheritance() -> None:
    """Тест __add__ с наследниками класса Product"""
    # Создаем простого наследника для теста
    class TestProduct(Product):
        pass

    product1 = TestProduct("Тест1", "Описание1", 100.0, 5)
    product2 = TestProduct("Тест2", "Описание2", 200.0, 3)

    # Должно работать, так как оба одного класса
    expected = (100.0 * 5) + (200.0 * 3)
    assert product1 + product2 == expected


def test_category_add_product_type_error_with_string() -> None:
    """Тест add_product с передачей строки вместо продукта"""
    category = Category("Тест", "Описание")

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
        category.add_product("это строка, а не продукт")  # type: ignore


def test_category_add_product_type_error_with_int() -> None:
    """Тест add_product с передачей числа вместо продукта"""
    category = Category("Тест", "Описание")

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
        category.add_product(12345)  # type: ignore


def test_category_add_product_type_error_with_list() -> None:
    """Тест add_product с передачей списка вместо продукта"""
    category = Category("Тест", "Описание")

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
        category.add_product([])  # type: ignore


def test_category_add_product_type_error_with_dict() -> None:
    """Тест add_product с передачей словаря вместо продукта"""
    category = Category("Тест", "Описание")

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
        category.add_product({})  # type: ignore


def test_category_add_product_with_none() -> None:
    """Тест add_product с передачей None"""
    category = Category("Тест", "Описание")

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
        category.add_product(None)  # type: ignore


def test_category_add_product_with_product_subclass() -> None:
    """Тест add_product с объектом класса-наследника Product"""
    # Создаем простого наследника
    class TestProduct(Product):
        def __init__(self, name, description, price, quantity, extra_param):
            super().__init__(name, description, price, quantity)
            self.extra_param = extra_param

    test_product = TestProduct("Тест", "Описание", 100.0, 5, "доп параметр")
    category = Category("Тест", "Описание")

    # Должно работать, так как TestProduct - наследник Product
    initial_count = Category.product_count
    initial_products_len = len(getattr(category, "_Category__products"))

    category.add_product(test_product)

    updated_products = getattr(category, "_Category__products")
    assert len(updated_products) == initial_products_len + 1
    assert updated_products[-1] == test_product
    assert Category.product_count == initial_count + 1


def test_product_add_method_different_subclasses() -> None:
    """Тест __add__ с разными наследниками Product (должно вызывать TypeError)"""
    # Создаем два разных класса-наследника
    class Smartphone(Product):
        pass

    class Laptop(Product):
        pass

    smartphone = Smartphone("iPhone", "Смартфон", 100000.0, 3)
    laptop = Laptop("MacBook", "Ноутбук", 150000.0, 2)

    # Проверяем, что type(self) is not type(other) вызывает TypeError
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
        smartphone + laptop


def test_product_add_method_same_subclass() -> None:
    """Тест __add__ с одинаковыми наследниками Product (должно работать)"""
    class Smartphone(Product):
        pass

    smartphone1 = Smartphone("iPhone", "Смартфон", 100000.0, 3)
    smartphone2 = Smartphone("Samsung", "Смартфон", 90000.0, 5)

    expected = (100000.0 * 3) + (90000.0 * 5)
    assert smartphone1 + smartphone2 == expected


def test_product_add_method_mixed_classes_detailed() -> None:
    """Детальный тест для проверки type() в __add__"""
    # Создаем продукты с разными типами
    product = Product("Обычный товар", "Описание", 100.0, 5)

    class ChildProduct(Product):
        pass

    child = ChildProduct("Дочерний товар", "Описание", 200.0, 3)

    # Проверяем, что type(product) is not type(child)
    assert type(product) is not type(child)

    # Проверяем, что сложение вызывает ошибку
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
        product + child

    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
        child + product


def test_product_add_method_same_type_with_subclass() -> None:
    """Тест, что __add__ с одинаковыми типами работает даже для подклассов"""
    class ChildProduct(Product):
        pass

    child1 = ChildProduct("Дочерний 1", "Описание", 100.0, 5)
    child2 = ChildProduct("Дочерний 2", "Описание", 200.0, 3)

    # Оба одного типа ChildProduct, поэтому должно работать
    expected = (100.0 * 5) + (200.0 * 3)
    assert child1 + child2 == expected


def test_category_product_count_with_add_and_quantity() -> None:
    """Тест, что product_count считает позиции, а не quantity"""
    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0

    # Создаем продукты с разным quantity
    p1 = Product("Товар 1", "Описание", 100.0, 10)  # quantity = 10
    p2 = Product("Товар 2", "Описание", 200.0, 5)   # quantity = 5

    # Создаем категорию с этими продуктами
    category = Category("Категория", "Описание", [p1, p2])

    # product_count должен быть 2 (количество позиций), а не 15 (сумма quantity)
    assert Category.product_count == 2

    # Добавляем еще один продукт
    p3 = Product("Товар 3", "Описание", 300.0, 3)
    category.add_product(p3)

    # product_count должен увеличиться на 1, а не на 3
    assert Category.product_count == 3

    # Проверяем, что __str__ показывает сумму quantity
    assert str(category) == "Категория, количество продуктов 18 шт."
