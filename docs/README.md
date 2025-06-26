# Django-todo-project

# 📡 OrderBridge

OrderBridge — платформа для замовників і виконавців із можливістю листування в реальному часі.

## 🚀 Основний стек

- Django 4.x
- Django Channels + Redis (WebSocket)
- PostgreSQL
- Bootstrap 5
- Celery (для фонових задач)

## 🛠️ Як розгорнути локально

```bash
git clone https://github.com/yourorg/orderbridge.git
cd orderbridge
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## 💬 WebSocket

- URL: `ws://localhost:8000/ws/chat/order/<order_id>/`
- Протокол:
  - `chat_message`: надходить при новому повідомленні або ставці
  - `chat_history`: надсилається при підʼєднанні для завантаження історії

## 📂 Структура каталогів

```bash
project/
├── chat/
│   ├── consumers.py
│   ├── templates/chat/
├── orders/
│   ├── models.py
│   ├── views.py
├── templates/
│   ├── base.html
│   ├── orders/
├── static/
├── manage.py
```

## 🧪 Тести

```bash
pytest
```

## 🧠 Автори

## Запуск сервера
uvicorn todo_manager.asgi:application --port 8080 --reload 

Команда GlazgloJon, 2025

