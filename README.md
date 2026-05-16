# Telegram Bot — деплой на Railway

## Файлы
- `bot.py` — основной код бота
- `requirements.txt` — зависимости
- `Procfile` — команда запуска
- `railway.json` — конфиг Railway

## Деплой на Railway

### 1. Загрузи файлы на GitHub
Создай репозиторий и залей все 4 файла.

### 2. Подключи Railway
- Зайди на https://railway.app
- New Project → Deploy from GitHub repo
- Выбери свой репозиторий

### 3. Добавь переменные окружения
В Railway: Settings → Variables → Add Variable

| Переменная | Значение |
|------------|----------|
| `BOT_TOKEN` | Токен от @BotFather |
| `ADMIN_ID` | `5703356053` |

### 4. Deploy
Railway автоматически запустит бота. Готово!

## Как пользоваться
- Пользователь пишет /start → вводит сообщение
- Тебе приходит уведомление с именем, @username и ID
- Нажимаешь "↩️ Ответить" → пишешь ответ → бот доставляет пользователю
