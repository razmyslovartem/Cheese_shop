from typing import List

from _pytest.capture import CaptureFixture

from src.category import Category, Product
import pytest


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
    return Category(
        "Тестовая категория товаров",
        "Тестовое описание товаров",
        [sample_product_1, sample_product_2]
    )


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

    category1 = Category("Категория 1", "Описание 1")
    assert Category.category_count == 1
    assert category1.name == "Категория 1"
    assert category1.description == "Описание 1"

    category2 = Category("Категория 2", "Описание 2")
    assert Category.category_count == 2
    assert category2.name == "Категория 2"
    assert category2.description == "Описание 2"


def test_product_count(sample_product_1: Product, sample_product_2: Product, sample_product_3: Product) -> None:
    """Тест на подсчет количества товаров во всех категориях"""
    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0

    # Категория с 2 товарами
    category1 = Category("Категория с товарами", "Описание", [sample_product_1, sample_product_2])
    assert Category.product_count == 2

    # Категория с 1 товаром
    category2 = Category("Еще категория", "Описание", [sample_product_3])
    assert Category.product_count == 3  # 2 + 1 = 3

    # Пустая категория
    category3 = Category("Пустая категория", "Описание")
    assert Category.product_count == 3  # не изменилось


def test_product_new_classmethod() -> None:
    """Тест класс-метода new_product"""
    product_data = {
        "name": "Тестовый продукт",
        "description": "Тестовое описание",
        "price": 999.99,
        "quantity": 10
    }

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