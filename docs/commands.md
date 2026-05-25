# Команды бота

---

# Пользовательские команды

## `/start`

Запуск бота.

---

## `/status`

Показывает статистику пользователя.

---

## `/settings`

Показывает настройки пользователя.

---

## `/prompt <text>`

Изменяет пользовательский prompt.

Пример:

```text
/prompt Пиши кратко и строго
```

---

## `/set-model <model>`

Изменяет модель пользователя.

Пример:

```text
/set-model mock
```

---

## `/set-temperature <value>`

Изменяет temperature пользователя.

Пример:

```text
/set-temperature 0.7
```

---

## `/set-max-tokens <value>`

Изменяет max tokens пользователя.

Пример:

```text
/set-max-tokens 1200
```

---

## `/new`

Создаёт новый чат.

Старый чат удаляется.

---

## `/reset`

Полностью удаляет текущий чат.

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

---

## `/admin-set-max-tokens <value>`

Изменяет глобальный лимит токенов.

---

## `/admin-set-temperature <value>`

Изменяет глобальный temperature.

---

## `/admin-allow-model-change <true|false>`

Разрешает или запрещает изменение модели пользователями.

---

## `/admin-allow-temperature-change <true|false>`

Разрешает или запрещает изменение temperature пользователями.

---

## `/admin-allow-max-tokens-change <true|false>`

Разрешает или запрещает изменение max tokens пользователями.

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
