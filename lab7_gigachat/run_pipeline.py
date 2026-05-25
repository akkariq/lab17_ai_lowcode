import json
from gigachat_client import GigaChatAssistant

def main():
    assistant = GigaChatAssistant()
    
    # 1. Тест генерации функций по ТЗ
    print("\n[1/4] Генерируем функцию валидации Email...")
    prompt_email = "Напиши функцию validate_email(email: str) -> bool для проверки корректности email через регулярное выражение."
    generated_email = assistant.generate_code(prompt_email)
    print("--- Сгенерированный код валидации ---")
    print(generated_email)
    
    # 2. Тест рефакторинга плохого кода
    print("\n[2/4] Читаем плохой код и отправляем на рефакторинг ИИ...")
    with open("bad_code.py", "r", encoding="utf-8") as f:
        bad_code = f.read()
        
    requirements = """
    1. Переименуй все функции и переменные в осмысленные имена по PEP8.
    2. Добавь аннотации типов (Type Hinting) и подробные docstrings.
    3. Замени глобальную переменную константой внутри функций или вынеси её.
    4. Добавь базовую обработку ошибок.
    """
    refactored_code = assistant.refactor_code(bad_code, requirements)
    
    with open("refactored_code.py", "w", encoding="utf-8") as f:
        f.write(refactored_code)
    print("✅ Отрефакторенный код успешно сохранен в refactored_code.py!")
    
    # 3. Автоматическая генерация тестов
    print("\n[3/4] Генерируем модульные тесты для нового кода...")
    generated_tests = assistant.generate_tests(refactored_code, framework="pytest")
    
    with open("test_refactored.py", "w", encoding="utf-8") as f:
        f.write(generated_tests)
    print("✅ Тесты на pytest успешно сохранены в test_refactored.py!")
    
    # 4. Анализ качества полученного кода
    print("\n[4/4] Запускаем ИИ-анализатор качества кода...")
    analysis_result = assistant.analyze_code(refactored_code)
    print("--- Результаты анализа качества (JSON) ---")
    print(json.dumps(analysis_result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()