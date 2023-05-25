import os
from dotenv import load_dotenv

load_dotenv()

# Валидные логин и пароль для входа
test_email = os.getenv('test_email')
test_password = os.getenv('test_password')

