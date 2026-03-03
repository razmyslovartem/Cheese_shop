from typing import List

from src.category import Category
from src.category import Product
import pytest


@pytest.fixture()
def sample_product_1() -> Product:  # переименовали
    return Product("Iphone 17 Pro", "1TB, Cosmic Orange", 189000.0, 3)


@pytest.fixture()
def sample_product_2() -> Product:  # добавили второй продукт
    return Product("Samsung Galaxy S25", "512GB, Phantom Black", 150000.0, 5)


@pytest.fixture()
def sample_product_3() -> Product:  # ДОБАВЛЯЕМ НЕДОСТАЮЩУЮ ФИКСТУРУ
    return Product("Xiaomi Mi 14", "256GB, Green", 50000.0, 10)


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


@pytest.fixture()
def sample_category(sample_product_1: Product, sample_product_2: Product) -> Category:
    return Category("Тестовая категория товаров", "Тестовое описание товаров", [sample_product_1, sample_product_2])


def test_category_products_list(sample_category: Category) -> None:
    """Тест с использованием List в аннотации"""
    products_list: List[Product] = sample_category.products  # ⬅ ЗДЕСЬ ИСПОЛЬЗУЕТСЯ List
    assert len(products_list) == 2
    assert products_list[0].name == "Iphone 17 Pro"


def test_init_category(sample_category: Category, sample_product_1: Product, sample_product_2: Product) -> None:
    """Тест на корректность инициализации объектов класса Category"""
    assert sample_category.name == "Тестовая категория товаров"
    assert sample_category.description == "Тестовое описание товаров"
    assert len(sample_category.products) == 2
    assert sample_category.products[0] == sample_product_1
    assert sample_category.products[1] == sample_product_2


def test_category_count() -> None:
    """Тест на подсчет количества категорий"""
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
    category3 = Category("Категория 3", "Описание 3")
    assert Category.category_count == 3
    assert category3.name == "Категория 3"
    assert category3.description == "Описание 3"


def test_product_count(sample_product_1: Product, sample_product_2: Product, sample_product_3: Product) -> None:
    """Тест на подсчет количества товаров в категориях"""
    Category.category_count = 0
    Category.product_count = 0

    category1 = Category("Категория с товарами", "Описание", [sample_product_1, sample_product_2])
    assert Category.product_count == 2
    assert len(category1.products) == 2
    assert category1.products[0] == sample_product_1
    assert category1.products[1] == sample_product_2
    assert category1.product_count == 2

    # Создаем категорию с 1 товаром
    category2 = Category("Еще категория", "Описание", [sample_product_3])
    assert Category.product_count == 3  # 2 + 1 = 3
    assert len(category2.products) == 1
    assert category2.products[0] == sample_product_3
    assert category2.product_count == 3

    # Создаем категорию без товаров
    category3 = Category("Пустая категория", "Описание")
    assert Category.product_count == 3  # не изменилось
    assert len(category3.products) == 0
    assert category3.product_count == 3
