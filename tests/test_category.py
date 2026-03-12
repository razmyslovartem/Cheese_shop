from _pytest.capture import CaptureFixture
from abc import ABC
import pytest

from src.category import Category
from src.category import Product
from src.category import Smartphone
from src.category import LawnGrass
from src.category import BaseProduct


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
def sample_smartphone() -> Smartphone:
    return Smartphone(
        name="iPhone 15",
        description="Флагманский смартфон",
        price=120000.0,
        quantity=10,
        efficiency=8.5,
        model="15 Pro",
        memory=512,
        color="Gray"
    )


@pytest.fixture()
def sample_lawn_grass() -> LawnGrass:
    return LawnGrass(
        name="Газон спортивный",
        description="Быстрорастущий газон",
        price=2500.0,
        quantity=20,
        country="Россия",
        germination_period="7-10 дней",
        color="Зеленый"
    )


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
    # Очищаем вывод от сообщения о создании объекта
    capsys.readouterr()

    product = Product("Тест", "Описание", 100.0, 5)
    # Очищаем вывод после создания продукта
    capsys.readouterr()

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


# НОВЫЕ ТЕСТЫ ДЛЯ ЗАДАНИЯ 3

def test_product_str_method(sample_product_1: Product) -> None:
    """Тест магического метода __str__ класса Product"""
    product_str = str(sample_product_1)
    expected = "Iphone 17 Pro, 189000 руб. Остаток: 3 шт."
    assert product_str == expected


def test_product_str_method_with_integer_price() -> None:
    """Тест __str__ с целочисленной ценой"""
    product = Product("Тест", "Описание", 100.0, 5)
    assert str(product) == "Тест, 100 руб. Остаток: 5 шт."


def test_product_str_method_with_float_price() -> None:
    """Тест __str__ с дробной ценой"""
    product = Product("Тест", "Описание", 99.99, 5)
    assert str(product) == "Тест, 99.99 руб. Остаток: 5 шт."


def test_category_str_method(sample_category: Category) -> None:
    """Тест магического метода __str__ класса Category"""
    category_str = str(sample_category)
    # Общее количество: 3 + 5 = 8
    expected = "Тестовая категория товаров, количество продуктов 8 шт."
    assert category_str == expected


def test_category_str_method_empty() -> None:
    """Тест __str__ для пустой категории"""
    category = Category("Пустая категория", "Описание")
    assert str(category) == "Пустая категория, количество продуктов 0 шт."


def test_category_str_method_single_product(sample_product_1: Product) -> None:
    """Тест __str__ для категории с одним продуктом"""
    category = Category("Категория с одним товаром", "Описание", [sample_product_1])
    assert str(category) == "Категория с одним товаром, количество продуктов 3 шт."


def test_product_add_method(sample_product_1: Product, sample_product_2: Product) -> None:
    """Тест магического метода __add__ класса Product"""
    # 189000 * 3 + 150000 * 5 = 567000 + 750000 = 1317000
    expected_sum = (189000.0 * 3) + (150000.0 * 5)
    assert sample_product_1 + sample_product_2 == expected_sum


def test_product_add_method_with_other_products(sample_product_2: Product, sample_product_3: Product) -> None:
    """Тест __add__ с другими продуктами"""
    # 150000 * 5 + 50000 * 10 = 750000 + 500000 = 1250000
    expected_sum = (150000.0 * 5) + (50000.0 * 10)
    assert sample_product_2 + sample_product_3 == expected_sum


def test_product_add_method_with_same_product(sample_product_1: Product) -> None:
    """Тест __add__ с тем же продуктом"""
    # 189000 * 3 + 189000 * 3 = 567000 + 567000 = 1134000
    expected_sum = (189000.0 * 3) * 2
    assert sample_product_1 + sample_product_1 == expected_sum


def test_product_add_method_type_error() -> None:
    """Тест __add__ с неправильным типом данных"""
    product = Product("Тест", "Описание", 100.0, 5)

    with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
        product + 10  # type: ignore

    with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
        product + "строка"  # type: ignore


def test_products_property_uses_str_method(sample_category: Category, monkeypatch) -> None:
    """Тест, что геттер products использует __str__ каждого продукта"""
    # Мокаем __str__ для продуктов, чтобы проверить, что он вызывается
    original_str = Product.__str__

    call_count = 0

    def mock_str(self):
        nonlocal call_count
        call_count += 1
        return original_str(self)

    monkeypatch.setattr(Product, "__str__", mock_str)

    # Вызываем геттер products
    _ = sample_category.products

    # Должен был вызваться для каждого продукта (2 раза)
    assert call_count == 2


def test_str_methods_integration(sample_category: Category, capsys) -> None:
    """Интеграционный тест для всех строковых методов"""
    # Очищаем вывод от сообщений о создании объектов
    capsys.readouterr()

    print(sample_category)
    captured = capsys.readouterr()
    assert "количество продуктов 8 шт." in captured.out

    print(sample_category.products)
    captured = capsys.readouterr()
    assert "Iphone 17 Pro" in captured.out
    assert "Samsung Galaxy S25" in captured.out

    for product in getattr(sample_category, "_Category__products"):
        print(product)
        captured = capsys.readouterr()
        assert "руб. Остаток:" in captured.out


def test_add_methods_integration() -> None:
    """Интеграционный тест для метода сложения"""
    p1 = Product("A", "Desc", 100, 10)
    p2 = Product("B", "Desc", 200, 5)
    p3 = Product("C", "Desc", 50, 20)

    # Проверяем разные комбинации сложения
    assert p1 + p2 == (100 * 10) + (200 * 5)
    assert p1 + p3 == (100 * 10) + (50 * 20)
    assert p2 + p3 == (200 * 5) + (50 * 20)

    # Проверяем, что результат можно использовать в вычислениях
    total = (p1 + p2) + (p1 + p3)
    expected = (100 * 10 + 200 * 5) + (100 * 10 + 50 * 20)
    assert total == expected


# НОВЫЕ ТЕСТЫ ДЛЯ ПРОВЕРКИ НОВОЙ ФУНКЦИОНАЛЬНОСТИ (5 штук)

def test_base_product_abstract() -> None:
    """Тест, что BaseProduct является абстрактным классом"""
    assert issubclass(BaseProduct, ABC)
    with pytest.raises(TypeError):
        BaseProduct()  # type: ignore


def test_smartphone_creation(sample_smartphone: Smartphone) -> None:
    """Тест создания смартфона"""
    assert sample_smartphone.name == "iPhone 15"
    assert sample_smartphone.description == "Флагманский смартфон"
    assert sample_smartphone.price == 120000.0
    assert sample_smartphone.quantity == 10
    assert sample_smartphone.efficiency == 8.5
    assert sample_smartphone.model == "15 Pro"
    assert sample_smartphone.memory == 512
    assert sample_smartphone.color == "Gray"


def test_lawn_grass_creation(sample_lawn_grass: LawnGrass) -> None:
    """Тест создания газонной травы"""
    assert sample_lawn_grass.name == "Газон спортивный"
    assert sample_lawn_grass.description == "Быстрорастущий газон"
    assert sample_lawn_grass.price == 2500.0
    assert sample_lawn_grass.quantity == 20
    assert sample_lawn_grass.country == "Россия"
    assert sample_lawn_grass.germination_period == "7-10 дней"
    assert sample_lawn_grass.color == "Зеленый"


def test_different_classes_cannot_add(sample_smartphone: Smartphone, sample_lawn_grass: LawnGrass) -> None:
    """Тест запрета сложения разных классов"""
    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
        sample_smartphone + sample_lawn_grass


def test_repr_mixin_output(capsys) -> None:
    """Тест, что миксин выводит сообщение при создании объекта"""
    # Очищаем предыдущий вывод
    capsys.readouterr()

    Product("Тест", "Описание", 100.0, 5)
    captured = capsys.readouterr()

    assert "Создан объект: Product(" in captured.out
    assert "name='Тест'" in captured.out
    assert "description='Описание'" in captured.out
    assert "quantity=5" in captured.out
