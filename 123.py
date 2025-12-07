import os
from dotenv import load_dotenv

# Загрузка переменных из .env-файла
load_dotenv()

# Пример получения значения переменной
api_key = os.getenv('API_KEY')
print(api_key)