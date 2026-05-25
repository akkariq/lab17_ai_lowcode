import os
import json
import logging
from dotenv import load_dotenv
from gigachat import GigaChat
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

class GigaChatAssistant:
    """Ассистент на базе GigaChat для автоматизации задач разработки (Генерация, Рефакторинг, Тесты)"""
    
    def __init__(self):
        self.credentials = os.getenv("GIGACHAT_CREDENTIALS")
        self.scope = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
        self.model = os.getenv("GIGACHAT_MODEL", "GigaChat-2")
        self.verify_ssl = os.getenv("GIGACHAT_VERIFY_SSL_CERTS", "False").lower() == "true"
        
        if not self.credentials:
            raise ValueError("Ошибка: GIGACHAT_CREDENTIALS не найден в переменных окружения или .env файле!")
            
        self.client = GigaChat(
            credentials=self.credentials,
            scope=self.scope,
            model=self.model,
            verify_ssl_certs=self.verify_ssl
        )
        logger.info(f"ИИ-Ассистент успешно инициализирован. Модель: {self.model}")
    
    def _clean_markdown(self, text: str, language: str = "python") -> str:
        """Вспомогательный метод очистки ответа ИИ от блоков ```python ... ```"""
        text = text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        return text

    def generate_code(self, description: str, language: str = "python") -> str:
        """Генерация кода по текстовому описанию с аннотациями типов и docstring"""
        prompt = f"""
        Ты — ведущий эксперт по разработке на {language}. Напиши чистый, рабочий код на {language} для следующей задачи:
        {description}
        
        Требования к коду:
        - Обязательно добавь аннотации типов (Type Hinting)
        - Добавь подробный docstring к функциям
        - Используй понятные имена переменных по PEP8
        - Добавь обработку исключений (try-except)
        
        Верни ТОЛЬКО чистый код. Никаких лишних слов, пояснений и комментариев вне кода.
        """
        response = self.client.chat(prompt)
        return self._clean_markdown(response.choices[0].message.content, language)
    
    def refactor_code(self, code: str, requirements: str) -> str:
        """Рефакторинг существующего кода по заданным требованиям"""
        prompt = f"""
        Проведи профессиональный рефакторинг следующего Python-кода.
        
        Исходный код:
        ```python
        {code}
        ```
        
        Требования к рефакторингу:
        {requirements}
        
        Дополнительные требования:
        - Полностью сохрани исходную бизнес-логику
        - Избавься от плохих имен, дублирования и глобальных переменных
        - Добавь аннотации типов и docstrings
        
        Верни ТОЛЬКО отрефакторенный код без текстовых пояснений.
        """
        response = self.client.chat(prompt)
        return self._clean_markdown(response.choices[0].message.content)
    
    def generate_tests(self, code: str, framework: str = "pytest") -> str:
        """Автоматическая генерация модульных тестов (позитивные, негативные, граничные случаи)"""
        prompt = f"""
        Напиши полноценные модульные тесты для следующего кода, используя фреймворк {framework}.
        
        Код для тестирования:
        ```python
        {code}
        ```
        
        Требования к тестам:
        - Протестируй все функции
        - Обязательно включи позитивные и негативные сценарии
        - Проверь граничные значения и обработку ошибок
        
        Верни ТОЛЬКО готовый код тестов, готовый к запуску через {framework}. Без лишних слов.
        """
        response = self.client.chat(prompt)
        return self._clean_markdown(response.choices[0].message.content)
    
    def analyze_code(self, code: str) -> Dict[str, List[str]]:
        """Критический анализ качества кода с выгрузкой отчета в формате JSON"""
        prompt = f"""
        Проанализируй качество, читаемость, производительность и безопасность следующего Python-кода.
        
        Код для анализа:
        ```python
        {code}
        ```
        
        Верни результат СТРОГО в формате валидного JSON-словаря (без markdown разметки json). Структура:
        {{
            "quality_issues": ["описание проблемы 1", "описание проблемы 2"],
            "readability_issues": ["описание проблемы 1"],
            "security_issues": ["уязвимости или пусто"],
            "performance_issues": ["проблемы со скоростью или пусто"],
            "suggestions": ["что конкретно исправить 1", "что исправить 2"]
        }}
        """
        response = self.client.chat(prompt)
        raw_content = response.choices[0].message.content.strip()
        
        if "```json" in raw_content:
            raw_content = raw_content.split("```json")[1].split("```")[0]
        elif "```" in raw_content:
            raw_content = raw_content.split("```")[1]
            
        try:
            return json.loads(raw_content.strip())
        except Exception:
            return {"error": ["Не удалось распарсить JSON"], "raw_response": [raw_content]}