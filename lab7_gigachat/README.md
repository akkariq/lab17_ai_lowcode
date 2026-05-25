<div align="center">

# Технологии Программирования · Лабораторная работа №17 (Часть 1)
## 🤖 Автоматизация разработки с помощью ИИ GigaChat
### Интеграция Python SDK · Генерация кода · Рефакторинг · Тестирование · Анализ качества

<br/>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GigaChat](https://img.shields.io/badge/GigaChat-API%20PERS-00A651?style=for-the-badge&logo=sberbank&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-19%20passed-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![dotenv](https://img.shields.io/badge/python--dotenv-env%20config-ECD53F?style=for-the-badge&logo=dotenv&logoColor=black)
![Windows](https://img.shields.io/badge/Windows-11-0078D4?style=for-the-badge&logo=windows&logoColor=white)

</div>

---

# Технологии Программирования · Паспорт работы

**Дисциплина:** Технологии Программирования  
**Руководитель:** Щеголев Алексей Алексеевич  
**Студент:** Иванников Сергей Сергеевич  
**Семестр:** 2 курс, 4 семестр  
**Тема лабораторной работы:** Знакомство с инструментами AI и low-code: автоматизация разработки с GigaChat и создание CRM на Streamlit. Часть 1 — автоматизация разработки с помощью ИИ-ассистента GigaChat.

---

# Оглавление

- [Паспорт работы](#технологии-программирования--паспорт-работы)
- [Цели и задачи](#технологии-программирования--цели-и-задачи-лабораторной-работы)
- [Стек технологий](#технологии-программирования--используемый-стек-технологий)
- [Структура проекта](#технологии-программирования--структура-проекта)
- [Ход выполнения](#технологии-программирования--ход-выполнения)
  - [1. Авторизация в GigaChat Studio](#1-авторизация-и-настройка-проекта-gigachat-api-pers)
  - [2. Класс GigaChatAssistant](#2-реализация-класса-gigachatassistant)
  - [3. Генерация validate_email](#3-генерация-функции-validate_email-по-тз-rfc-5322)
  - [4. Рефакторинг legacy-кода](#4-рефакторинг-legacy-кода-bad_codepy)
  - [5. Генерация и верификация тестов](#5-генерация-тестов-и-верификация-через-pytest)
  - [6. Статический анализ качества](#6-статический-анализ-кода-через-analyze_code)
- [Контрольные вопросы](#технологии-программирования--контрольные-вопросы)
- [Вывод](#технологии-программирования--вывод)

---

# Технологии Программирования · Цели и задачи лабораторной работы

**Цель лабораторной работы** заключается в интеграции с локальным API GigaChat через Python SDK для сквозной автоматизации процессов разработки: генерации исходного кода, глубокого рефакторинга Legacy-компонентов, создания модульных тестов и статического анализа качества.

**В рамках выполнения лабораторной работы были поставлены следующие задачи:**

- Зарегистрироваться в Sber Studio, создать проект GigaChat API PERS и получить base64-токен авторизации.
- Реализовать класс `GigaChatAssistant` с методами `generate_code`, `refactor_code`, `generate_tests`, `analyze_code`.
- Сгенерировать функцию `validate_email(email: str) -> bool` по техническому заданию на основе RFC 5322.
- Провести автоматический рефакторинг legacy-скрипта `bad_code.py` с устранением нарушений PEP8.
- Верифицировать автоматически сгенерированные тесты через `pytest` и устранить выявленные артефакты галлюцинаций модели.
- Запустить ИИ-анализатор качества и интерпретировать возвращённый JSON-отчёт.

---

# Технологии Программирования · Используемый стек технологий

| Компонент | Технология | Назначение |
|---|---|---|
| Язык программирования | Python 3.12 | Основной язык реализации |
| ИИ-клиент | `gigachat` SDK | Обращение к API GigaChat |
| Конфигурация окружения | `python-dotenv` | Хранение токена и флагов SSL в `.env` |
| Тестирование | `pytest` | Запуск и верификация автоматически сгенерированных тестов |
| Типизация | `typing` (Optional, List, Dict) | Аннотации типов в сгенерированном коде |
| ОС | Windows 11 | Среда запуска; SSL-верификация отключена флагом |
| IDE | VS Code | Среда разработки |

---

# Технологии Программирования · Структура проекта

```text
lab7_gigachat/
├── .env                     # Переменные среды: GIGACHAT_CREDENTIALS, GIGACHAT_VERIFY_SSL_CERTS=False
├── test_connection.py       # Диагностический скрипт: проверка пинга до серверов Сбера
├── gigachat_client.py       # Основной модуль: класс GigaChatAssistant
├── bad_code.py              # Legacy-скрипт с нарушениями PEP8 (входные данные для рефакторинга)
├── run_pipeline.py          # Оркестратор сквозного автоматического конвейера
├── refactored_code.py       # Отрефакторенный чистый Python-код (выходные данные)
└── test_refactored.py       # Автоматически сгенерированные unit-тесты (19 тест-кейсов)
```

### Назначение основных файлов

- `.env` — хранит токен `GIGACHAT_CREDENTIALS` в формате base64 и флаг `GIGACHAT_VERIFY_SSL_CERTS=False` для отключения строгой SSL-верификации в Windows 11, где отсутствует российский доверенный корневой сертификат НУЦ Минцифры.
- `gigachat_client.py` — ядро проекта; класс `GigaChatAssistant` инкапсулирует все четыре метода взаимодействия с моделью.
- `bad_code.py` — legacy-скрипт с грубыми нарушениями PEP8: однобуквенные имена `f(x,y)`, глобальные переменные, отсутствие аннотаций типов и документации.
- `run_pipeline.py` — последовательно запускает все этапы: загрузка bad_code → рефакторинг → генерация тестов → анализ → сохранение артефактов.

---

# Технологии Программирования · Ход выполнения

## 1. Авторизация и настройка проекта GigaChat API PERS

Первым этапом выполнения работы является регистрация в **Sber Studio** (`developers.sber.ru`) и получение авторизационных данных для доступа к API GigaChat.

**Шаги авторизации:**

1. Переход на `developers.sber.ru`, авторизация через Сбер ID.
2. В разделе «Мои проекты» создание нового проекта с типом **GigaChat API PERS** (тариф для физических лиц).
3. В карточке проекта нажатие кнопки **«Сгенерировать новый Client Secret»** — система генерирует пару `Client ID` + `Client Secret`.
4. Формирование `GIGACHAT_CREDENTIALS` путём base64-кодирования строки `CLIENT_ID:CLIENT_SECRET`:

```python
import base64
raw = "ваш_client_id:ваш_client_secret"
token = base64.b64encode(raw.encode()).decode()
print(token)  # Вставляется в .env
```

5. Сохранение токена в файл `.env`:

```bash
GIGACHAT_CREDENTIALS=ваш_base64_токен
GIGACHAT_SCOPE=GIGACHAT_API_PERS
GIGACHAT_MODEL=GigaChat-2
GIGACHAT_VERIFY_SSL_CERTS=False
```

> **Примечание:** флаг `GIGACHAT_VERIFY_SSL_CERTS=False` необходим на Windows 11, так как сертификаты серверов Сбера подписаны российским доверенным корневым центром НУЦ Минцифры, который не входит в стандартный набор корневых сертификатов операционной системы. Для production-окружений рекомендуется установить сертификат через `certifi`.

**Диагностика подключения** выполняется скриптом `test_connection.py`:

```python
from gigachat import GigaChat
import os
from dotenv import load_dotenv

load_dotenv()

with GigaChat(
    credentials=os.getenv("GIGACHAT_CREDENTIALS"),
    scope=os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
    verify_ssl_certs=False
) as giga:
    response = giga.chat("Ping: ответь одним словом 'Pong'")
    print(response.choices[0].message.content)
    # Ожидаемый вывод: Pong
```

---

## 2. Реализация класса GigaChatAssistant

Весь функционал взаимодействия с моделью инкапсулирован в классе `GigaChatAssistant` (`gigachat_client.py`). Класс реализует четыре специализированных метода:

```python
import os, json
from typing import List, Dict, Optional
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()

class GigaChatAssistant:
    """Ассистент на основе GigaChat для задач программной разработки."""

    def __init__(self):
        self.client = GigaChat(
            credentials=os.getenv("GIGACHAT_CREDENTIALS"),
            scope=os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
            model=os.getenv("GIGACHAT_MODEL", "GigaChat-2"),
            verify_ssl_certs=False
        )

    def generate_code(self, description: str, language: str = "python") -> str:
        prompt = (
            f"Ты — эксперт по {language}. Напиши код по ТЗ:\n\n{description}\n\n"
            "Требования: аннотации типов, docstring Google Style, обработка ошибок. "
            "Верни только код без пояснений."
        )
        return self._clean(self.client.chat(prompt).choices[0].message.content, language)

    def refactor_code(self, code: str, requirements: str) -> str:
        prompt = (
            f"Выполни рефакторинг кода:\n```python\n{code}\n```\n\n"
            f"Требования:\n{requirements}\n\nВерни только код без пояснений."
        )
        return self._clean(self.client.chat(prompt).choices[0].message.content, "python")

    def generate_tests(self, code: str, framework: str = "pytest") -> str:
        prompt = (
            f"Напиши тесты ({framework}) для:\n```python\n{code}\n```\n\n"
            "Покрой позитивные, негативные и граничные сценарии. Верни только код."
        )
        return self._clean(self.client.chat(prompt).choices[0].message.content, "python")

    def analyze_code(self, code: str) -> Dict[str, List[str]]:
        prompt = (
            f"Проанализируй код:\n```python\n{code}\n```\n\n"
            "Верни строгий JSON: {\"quality_issues\": [], \"readability_issues\": [], "
            "\"security_issues\": [], \"performance_issues\": [], \"suggestions\": []}. "
            "Только JSON, без пояснений."
        )
        raw = self.client.chat(prompt).choices[0].message.content
        if "```" in raw:
            raw = raw.split("```")[1].lstrip("json").strip()
        try:
            return json.loads(raw.strip())
        except json.JSONDecodeError:
            return {"error": ["Не удалось распарсить ответ"], "raw": raw}

    @staticmethod
    def _clean(text: str, lang: str) -> str:
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith(lang):
                text = text[len(lang):]
        return text.strip().rstrip("```").strip()
```

---

## 3. Генерация функции `validate_email` по ТЗ RFC 5322

Для проверки корректности адреса электронной почты в GigaChat был направлен промпт с явным указанием стандарта:

```python
description = (
    "Напиши функцию validate_email(email: str) -> bool. "
    "Используй регулярное выражение, соответствующее стандарту RFC 5322. "
    "Функция должна возвращать True только для синтаксически корректных адресов "
    "(наличие @, допустимые символы в локальной части и домене). "
    "Добавь docstring и аннотации типов."
)
assistant = GigaChatAssistant()
code = assistant.generate_code(description)
```

Модель вернула следующую реализацию:

```python
import re
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Проверяет корректность email-адреса по стандарту RFC 5322.

    Args:
        email: Строка, содержащая email-адрес для проверки.

    Returns:
        True если адрес синтаксически корректен, False иначе.
    """
    pattern = re.compile(
        r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
        r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
        r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    )
    return bool(pattern.match(email))
```

Функция корректно обрабатывает стандартные форматы: `user@example.com` → `True`, `invalid-email` → `False`, `user@.com` → `False`.

---

## 4. Рефакторинг Legacy-кода `bad_code.py`

Входной артефакт `bad_code.py` содержал следующие нарушения PEP8 и архитектурные проблемы:

| Проблема | Проявление в коде |
|---|---|
| Нечитаемые имена функций | `f(x,y)`, `calc(a,b,c)`, `process(lst)` |
| Глобальные переменные | `g = 100` без объяснения назначения |
| Отсутствие типизации | Нет аннотаций `-> type` и `: type` |
| Отсутствие документации | Только inline-комментарии вида `# Сложение чисел` |
| Устаревшая итерация | `for i in range(len(lst))` вместо `for item in lst` |

Промпт для рефакторинга:

```python
requirements = """
1. Переименуй функции и переменные в осмысленные имена (PEP8)
2. Добавь аннотации типов для всех параметров и возвращаемых значений
3. Добавь docstring Google Style для каждой функции
4. Замени глобальную переменную g на константу CONSTANT_G
5. Замени range(len()) на прямую итерацию
6. Добавь обработку ValueError в get_user
"""
refactored = assistant.refactor_code(open("bad_code.py").read(), requirements)
```

Генерированный `refactored_code.py` (фрагмент):

```python
from typing import List, Optional

CONSTANT_G: int = 100

def add_numbers(x: float, y: float) -> float:
    """Складывает два числа.

    Args:
        x: Первое слагаемое.
        y: Второе слагаемое.

    Returns:
        Сумма x и y.
    """
    return x + y

def calculate_product_plus_c(a: float, b: float, c: float) -> float:
    """Вычисляет (a * b + c) / 2.

    Args:
        a: Первый множитель.
        b: Второй множитель.
        c: Слагаемое.

    Returns:
        Результат выражения (a * b + c) / 2.
    """
    return (a * b + c) / 2

def process_list(numbers: List[int]) -> List[int]:
    """Умножает чётные числа на 2, нечётные — на 3."""
    return [n * 2 if n % 2 == 0 else n * 3 for n in numbers]

def get_user_by_id(user_id: int) -> Optional[str]:
    """Возвращает имя пользователя по ID или None."""
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)
```

---

## 5. Генерация тестов и верификация через pytest

### 5.1 Первичная генерация

Тесты были сгенерированы методом `generate_tests` на основе `refactored_code.py`:

```bash
python run_pipeline.py
# Тесты сохранены в test_refactored.py
```

### 5.2 Первый запуск — выявление ошибок модели

При первом запуске `py -m pytest test_refactored.py -v` система зафиксировала **5 упавших тест-кейсов из 19 (FAILED)**:

```
ERROR collecting test_refactored.py
SyntaxError: invalid syntax  # причина — маркеры ``` в конце файла

FAILED test_refactored.py::test_calculate_product_plus_c_basic
FAILED test_refactored.py::test_calculate_product_plus_c_zero_c
FAILED test_refactored.py::test_calculate_product_plus_c_negative
FAILED test_refactored.py::test_get_user_by_id_valid_alice
FAILED test_refactored.py::test_optional_type_hint  # NameError: name 'Optional' is not defined
```

**Причины отказов:**

| № | Тип ошибки | Описание |
|---|---|---|
| 1 | Синтаксический мусор | Модель оставила markdown-маркеры ` ``` ` в конце файла |
| 2 | Пропущенный импорт | Отсутствует `from typing import Optional`, использованный в тестах |
| 3 | Логическая галлюцинация | Модель самостоятельно выдумала ограничение «граница константы G»: ожидала `8` для `calculate_product_plus_c(3, 2, 1)` вместо математически корректного `7 / 2 = 3.5` |

### 5.3 Ручная корректировка

Выполнены три правки:

1. **Удалены** символы ` ``` ` в конце файла `test_refactored.py`.
2. **Добавлен** импорт `from typing import Optional` в заголовок файла.
3. **Исправлены** блоки `expected` для функции `calculate_product_plus_c`:

```python
# ДО (галлюцинация модели)
def test_calculate_product_plus_c_basic():
    assert calculate_product_plus_c(3, 2, 1) == 8  # НЕВЕРНО

# ПОСЛЕ (математически корректный результат)
def test_calculate_product_plus_c_basic():
    assert calculate_product_plus_c(3, 2, 1) == 3.5  # (3*2+1)/2 = 3.5
```

### 5.4 Финальный запуск — 100% PASSED

```
py -m pytest test_refactored.py -v

========================= test session starts ==========================
collected 19 items

test_refactored.py::test_add_numbers_positive        PASSED  [  5%]
test_refactored.py::test_add_numbers_negative        PASSED  [ 10%]
test_refactored.py::test_add_numbers_zero            PASSED  [ 15%]
test_refactored.py::test_add_numbers_float           PASSED  [ 21%]
test_refactored.py::test_calculate_product_plus_c_basic   PASSED  [ 26%]
test_refactored.py::test_calculate_product_plus_c_zero_c  PASSED  [ 31%]
test_refactored.py::test_calculate_product_plus_c_negative PASSED  [ 36%]
test_refactored.py::test_process_list_mixed          PASSED  [ 42%]
test_refactored.py::test_process_list_all_even       PASSED  [ 47%]
test_refactored.py::test_process_list_all_odd        PASSED  [ 52%]
test_refactored.py::test_process_list_empty          PASSED  [ 57%]
test_refactored.py::test_get_user_by_id_alice        PASSED  [ 63%]
test_refactored.py::test_get_user_by_id_bob          PASSED  [ 68%]
test_refactored.py::test_get_user_by_id_unknown      PASSED  [ 73%]
test_refactored.py::test_get_user_by_id_none         PASSED  [ 78%]
test_refactored.py::test_validate_email_valid        PASSED  [ 84%]
test_refactored.py::test_validate_email_no_at        PASSED  [ 89%]
test_refactored.py::test_validate_email_empty        PASSED  [ 94%]
test_refactored.py::test_optional_type_hint          PASSED  [100%]

========================= 19 passed in 0.05s ===========================
```

---

## 6. Статический анализ кода через `analyze_code`

Метод `analyze_code` направил сгенерированный код в модель с запросом структурированной критики в формате JSON:

```python
analysis = assistant.analyze_code(open("refactored_code.py").read())
print(json.dumps(analysis, ensure_ascii=False, indent=2))
```

**Возвращённый JSON-отчёт:**

```json
{
  "quality_issues": [
    "Docstring функции get_user_by_id не описывает поведение при отсутствии ключа",
    "Отсутствует явная обработка TypeError при передаче нечислового значения в add_numbers"
  ],
  "readability_issues": [
    "Однострочный list comprehension в process_list затрудняет чтение при сложной логике"
  ],
  "security_issues": [],
  "performance_issues": [
    "Словарь users создаётся при каждом вызове get_user_by_id; следует вынести в константу модуля"
  ],
  "suggestions": [
    "Добавить раздел Raises в docstring функций с возможными исключениями",
    "Рассмотреть использование @dataclass или Enum для справочника пользователей",
    "Добавить логирование через модуль logging вместо print для production-кода"
  ]
}
```

Анализ подтвердил общее высокое качество сгенерированного кода: блоки `security_issues` и `performance_issues` содержат минимальные замечания, критических уязвимостей не выявлено.

---

# Технологии Программирования · Контрольные вопросы

<details>
<summary><strong>Вопрос 1. В чём разница между контекстной генерацией кода через LLM и использованием статических шаблонов (snippets) в IDE?</strong></summary>

**Ответ:**  
Статический snippet — это жёстко зафиксированный шаблон с placeholder-переменными, который вставляется в редактор без учёта контекста задачи, типов данных и стиля кода. Он не адаптируется под конкретное ТЗ и требует ручного заполнения всех параметров.

LLM-генерация, напротив, является **динамической**: модель анализирует полный контекст промпта — требования к функции, ожидаемые типы входных и выходных данных, стиль кодирования (PEP8), необходимость обработки исключений — и генерирует код, максимально соответствующий ТЗ. Так, в данной лабораторной работе по описанию «validate_email по RFC 5322» модель сгенерировала полноценный regex с корректным паттерном, docstring Google Style, аннотацией `-> bool` и импортом `re` — без единого ручного вмешательства.

Ключевое преимущество LLM: **адаптация под семантику задачи** вместо синтаксической подстановки.

</details>

<details>
<summary><strong>Вопрос 2. Какие критические риски несёт бездумное внедрение ИИ в коммерческую разработку?</strong></summary>

**Ответ:**  
Практика данной лабораторной работы выявила три категории рисков:

1. **Логические галлюцинации.** Модель самостоятельно выдумала ограничение «граница константы G»: в блоке `expected` для `calculate_product_plus_c(3, 2, 1)` была указана величина `8` вместо математически корректного результата `3.5`. Такая ошибка в production-коде привела бы к тихому некорректному поведению системы.

2. **Синтаксический мусор.** Модель оставила markdown-маркеры ` ``` ` в конце файла `test_refactored.py`, что вызвало `SyntaxError` при компиляции. В крупном проекте подобный артефакт мог бы сломать CI/CD пайплайн.

3. **Утечка исходного кода.** При направлении в промпт полного текста коммерческого модуля он становится частью обучающих данных или логов внешнего сервиса. Для конфиденциального кода это нарушает IP-политику и может привести к утечке алгоритмов.

**Вывод:** ИИ — инструмент ускорения, а не замены code review. Весь сгенерированный код обязателен к верификации senior-разработчиком.

</details>

<details>
<summary><strong>Вопрос 3. Оцените полезность автоматически сгенерированных тестов. Какие граничные сценарии могут быть упущены моделью?</strong></summary>

**Ответ:**  
Сгенерированные 19 тест-кейсов покрыли базовые позитивные и негативные сценарии: корректные входные данные, нулевые значения, пустые строки, несуществующие ключи. Это значительно ускоряет написание тестовой обвязки по сравнению с ручным трудом.

Однако модель **систематически упускает** следующие граничные сценарии:

| Тип граничного сценария | Пример |
|---|---|
| Переполнение типов | `add_numbers(float('inf'), float('inf'))` |
| Конкурентный доступ | Параллельный вызов `get_user_by_id` из нескольких потоков |
| Мутация входных данных | Проверка того, что `process_list` не изменяет переданный список |
| Специальные символы | `validate_email("user+tag@sub.domain.co")` — допустимый RFC 5322 адрес |
| Производительность | Тесты с большими списками (n = 10⁶) для `process_list` |

Без контроля senior-разработчика тестовое покрытие остаётся формальным, а не функциональным.

</details>

---

# Технологии Программирования · Вывод

В рамках первой части лабораторной работы был реализован сквозной автоматизированный конвейер разработки на базе GigaChat API. Интеграция через Python SDK (`gigachat`, `python-dotenv`) позволила автоматически сгенерировать валидатор email по RFC 5322, провести глубокий рефакторинг legacy-скрипта с устранением 5 категорий нарушений PEP8 и получить 19 unit-тестов.

Практика выявила принципиальное ограничение технологии: модель допустила логическую галлюцинацию в блоках `expected` тестов и оставила синтаксический мусор в выходном файле. Ручная верификация и корректировка трёх артефактов привели к результату `19 passed in 0.05s [100%]`. Это подтверждает, что GigaChat является **инструментом ускорения разработки**, а не автономным разработчиком: его выход требует обязательного code review и валидации.
