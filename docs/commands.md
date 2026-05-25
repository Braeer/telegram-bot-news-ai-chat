# Команды бота

---

# Пользовательские команды

## `/start`

Запуск бота.

---

## `/status`

Показывает статистику пользователя.

Пример:

```text
Статистика:

Запросов: 0
Input tokens: 0
Output tokens: 0
Всего tokens: 0
Последний запрос: нет данных
```

---

## `/settings`

Показывает итоговые настройки пользователя.

Пример:

```text
Настройки:

Модель: mock
Temperature: 0.7
Max tokens: 2000

Prompt:
не задан
```

---

## `/prompt <text>`

Обновляет пользовательский prompt.

Пример:

```text
/prompt Пиши новости коротко и строго
```

---

## `/set-model <model>`

Изменяет модель пользователя.

Пример:

```text
/set-model gpt-4.1-mini
```

---

# Административные команды

## `/admin-data`

Показывает информацию о боте.

---

## `/admin-tokens`

Показывает статистику токенов.

---

## `/admin-settings`

Показывает глобальные настройки.

---

## `/admin-set-model <model>`

Изменяет глобальную модель.

Пример:

```text
/admin-set-model gpt-4.1-mini
```

---

## `/admin-set-max-tokens <value>`

Изменяет глобальный лимит токенов.

Пример:

```text
/admin-set-max-tokens 2000
```

---

## `/admin-allow-model-change <true|false>`

Разрешает или запрещает пользователям менять модель.

Пример:

```text
/admin-allow-model-change false
```

---

## `/add-user <telegram_user_id>`

Добавляет пользователя.

Пример:

```text
/add-user 123456
```

---

## `/add-admin <telegram_user_id>`

Добавляет администратора.

Пример:

```text
/add-admin 123456
```
