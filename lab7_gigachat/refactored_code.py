from typing import List, Optional

# Константа заменяет глобальную переменную
CONST_G = 100


def add_numbers(x: int, y: int) -> int:
    """Возвращает сумму двух чисел"""
    return x + y


def calculate_product_plus_c(a: float, b: float, c: float) -> float:
    """
    Рассчитывает выражение a * b + c / 2
    :param a: число
    :param b: число
    :param c: число
    :return: результат вычисления
    """
    product = a * b
    result = product + c
    return result / 2


def double_even_items(lst: List[int]) -> List[int]:
    """
    Возвращает список удвоенных четных элементов списка,
    остальные элементы утраиваются
    :param lst: входной список целых чисел
    :return: новый список преобразованных значений
    """
    result = []
    for item in lst:
        if item % 2 == 0:
            result.append(item * 2)
        else:
            result.append(item * 3)
    return result


def get_person_name(user_id: int) -> Optional[str]:
    """
    Возвращает имя пользователя по идентификатору
    :param user_id: уникальный идентификатор пользователя
    :return: строка имени пользователя или None
    """
    if user_id == 1:
        return 'Alice'
    elif user_id == 2:
        return 'Bob'
    return None