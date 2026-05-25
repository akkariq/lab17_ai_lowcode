import os
from dotenv import load_dotenv
from gigachat import GigaChat

# Загружаем ключи из .env
load_dotenv()
credentials = os.getenv("GIGACHAT_CREDENTIALS")

print("Устанавливаем безопасное соединение с GigaChat API...")

# verify_ssl_certs=False решает проблему с системными сертификатами в Windows
with GigaChat(credentials=credentials, verify_ssl_certs=False) as giga:
    try:
        response = giga.chat(
            "Привет! Если подключение работает, напиши фразу: 'Связь с сервером Сбера успешно установлена!'"
        )
        print("\n=== ОТВЕТ ОТ НЕЙРОСЕТИ ===")
        print(response.choices[0].message.content)
        print("==========================\n")
    except Exception as e:
        print(f"\n❌ Ошибка авторизации или запроса: {e}")