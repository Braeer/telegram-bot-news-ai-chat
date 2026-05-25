# telegram-bot-news-ai-chat

Telegram-бот для работы с ChatGPT API.

Бот помогает писать тексты и новости в заданном стиле, хранит персональные настройки пользователя и поддерживает административную панель.

---

# Возможности

- авторизация пользователей по Telegram userId
- middleware-проверка доступа
- пользовательские настройки
- глобальные настройки
- персональный prompt
- аналитика пользователей
- автоочистка чатов
- хранение данных в JSON
- fallback для неизвестных команд
- Docker-ready архитектура

---

# Технологии

- Python 3.12
- aiogram 3
- APScheduler
- python-dotenv
- Pytest
- Ruff
- Docker

---

# Структура проекта

```text
app/
  handlers/
  middlewares/
  services/
  storage/
  templates/
  utils/
  config/

data/
  analytics/
  chats/
  settings/

docs/
```

---

# Запуск

## Локально

```bash
python -m app.main
```

---

# Тестирование

```bash
python -m pytest
```

---

# Документация

Команды бота:

```text
docs/commands.md
```

---

# Статус проекта

Проект находится в активной разработке.
