import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters, ConversationHandler
)

# ===== НАСТРОЙКИ =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "5703356053"))
# =====================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

WAITING_MESSAGE = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Что бы ты хотел написать владельцу?\n\nНапиши своё сообщение:"
    )
    return WAITING_MESSAGE


async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if not user.username:
        await update.message.reply_text(
            "⚠️ У тебя нет username в Telegram!\n\n"
            "Пожалуйста, создай его:\n"
            "Настройки → Изменить профиль → Имя пользователя\n\n"
            "После этого напиши мне снова — иначе владелец не поймёт кто написал."
        )
        return ConversationHandler.END

    username = f"@{user.username}"
    full_name = user.full_name
    user_id = user.id

    forward_text = (
        f"📩 Новое сообщение!\n\n"
        f"👤 Имя: {full_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 ID: `{user_id}`\n\n"
        f"💬 Сообщение:\n{text}"
    )

    keyboard = [[InlineKeyboardButton("↩️ Ответить", callback_data=f"reply_{user_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=forward_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    await update.message.reply_text("✅ Твоё сообщение отправлено! Ожидай ответа.")
    return ConversationHandler.END


async def reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    user_id = int(query.data.split("_")[1])
    context.user_data["reply_to"] = user_id

    await query.message.reply_text("✏️ Напиши свой ответ:")


async def send_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    reply_to = context.user_data.get("reply_to")
    if not reply_to:
        return

    await context.bot.send_message(
        chat_id=reply_to,
        text=f"📬 Ответ от владельца:\n\n{update.message.text}"
    )

    await update.message.reply_text("✅ Ответ отправлен!")
    context.user_data.pop("reply_to", None)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Отменено.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(reply_button, pattern="^reply_"))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_ID),
        send_reply
    ))

    logger.info("Бот запущен!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
