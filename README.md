# telegram-bot-news-ai-chat

Telegram-бот для работы с ChatGPT API.

Бот помогает писать тексты и новости в заданном стиле, хранит персональные настройки пользователя и поддерживает административную панель.

---

# Возможности

- авторизация пользователей по Telegram userId
- middleware-проверка доступа
- персональные настройки пользователя
- глобальные настройки бота
- prompt для каждого пользователя
- хранение чатов
- автоочистка сообщений старше 2 дней
- аналитика пользователей
- mock AI без OpenAI токена
- Docker-ready архитектура
- rate limit middleware
- error middleware
- fallback для неизвестных команд
- unit тесты

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
  config/
  handlers/
  middlewares/
  services/
  storage/
  templates/
  utils/

data/
  analytics/
  chats/
  settings/

docs/
tests/
```

---

# Docker

## Запуск

```bash
docker compose up --build
```

## Логи

```bash
docker compose logs -f
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
