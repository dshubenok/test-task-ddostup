# Проект автоматизации входа в Gmail

Этот проект — тестовое задание для компании ddostup.ru

## Требования

- Python 3.12 или выше
- Android SDK
- Appium Server
- Android эмулятор или реальное устройство Android
- Gmail приложение, установленное на устройстве

## Установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/dshubenok/test-task-ddostup.git
   cd test-task-ddostup
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```
   python3 -m venv venv
   source venv/bin/activate  # Для Unix или MacOS
   venv\Scripts\activate  # Для Windows
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

## Настройка

1. Убедитесь, что у вас установлен и настроен Android SDK.

2. Запустите Appium Server. Вы можете сделать это через командную строку:

3. Подготовьте Android эмулятор или подключите реальное устройство Android.

4. Убедитесь, что на устройстве установлено приложение Gmail.

## Использование

1. Откройте файл `test_google_auth.py` и замените учетные данные на свои:
   ```python
   auth.login('your-email@gmail.com', 'your-password')
   ```

2. Запустите скрипт:
   ```
   python test_google_auth.py
   ```

3. Наблюдайте за процессом автоматического входа в Gmail на вашем устройстве :)
