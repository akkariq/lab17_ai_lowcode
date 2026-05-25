import pytest
from typing import Optional
from refactored_code import (add_numbers, 
                             calculate_product_plus_c, 
                             double_even_items, 
                             get_person_name)

# =====================================================================
# 1. Тестирование функции add_numbers (Сложение чисел)
# =====================================================================
@pytest.mark.parametrize("x, y, expected", [
    (1, 2, 3),
    (-5, 7, 2),
    (0, 0, 0),
    (99, 1, 100),
])
def test_add_numbers(x: int, y: int, expected: int):
    assert add_numbers(x, y) == expected


# =====================================================================
# 2. Тестирование функции calculate_product_plus_c (((a * b) + c) / 2)
# =====================================================================
@pytest.mark.parametrize("a, b, c, expected", [
    (2, 4, 6, 7.0),          # ((2 * 4) + 6) / 2 = 14 / 2 = 7.0
    (1, 1, 1, 1.0),          # ((1 * 1) + 1) / 2 = 2 / 2 = 1.0
    (0, 0, 100, 50.0),       # ((0 * 0) + 100) / 2 = 100 / 2 = 50.0
    (10, 10, -100, 0.0),     # ((10 * 10) - 100) / 2 = 0 / 2 = 0.0
    (0.5, 2, 1, 1.0),        # ((0.5 * 2) + 1) / 2 = 2 / 2 = 1.0
    (100, 1, 100, 100.0)     # ((100 * 1) + 100) / 2 = 200 / 2 = 100.0
])
def test_calculate_product_plus_c(a: float, b: float, c: float, expected: float):
    assert calculate_product_plus_c(a, b, c) == pytest.approx(expected, rel=1e-6)


# =====================================================================
# 3. Тестирование функции double_even_items (Четные * 2, Нечетные * 3)
# =====================================================================
@pytest.mark.parametrize("lst, expected", [
    ([1, 2, 3], [3, 4, 9]),               # 1*3=3 (нечет), 2*2=4 (чет), 3*3=9 (нечет)
    ([2, 4, 6], [4, 8, 12]),              # Все четные умножаются на 2
    ([1, 3, 5], [3, 9, 15]),              # Все нечетные умножаются на 3
    ([0, 0, 0], [0, 0, 0]),               # Нули (четные) умножаются на 2
    ([100, 100, 100], [200, 200, 200]),   # Все четные умножаются на 2
])
def test_double_even_items(lst: list, expected: list):
    assert double_even_items(lst) == expected


# =====================================================================
# 4. Тестирование функции get_person_name (Поиск по ID)
# =====================================================================
@pytest.mark.parametrize("user_id, expected", [
    (1, 'Alice'),
    (2, 'Bob'),
    (3, None),        # Отсутствие пользователя в базе
    (None, None),     # Некорректный ID
])
def test_get_person_name(user_id: Optional[int], expected: Optional[str]):
    assert get_person_name(user_id) == expected