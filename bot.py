import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# Palabras prohibidas
BANNED_WORDS = [
    "coca", "cocaina", "falopa", "porro", "marihuana", "vendo",
    "venta", "droga", "mdma", "tussi", "ketamina", "lsd"
]

async def moderate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text.lower()

        for word in BANNED_WORDS:
            if word in text:
                user = update.message.from_user

                # Borrar mensaje
                await update.message.delete()

                # Banear usuario
                await context.bot.ban_chat_member(
                    chat_id=update.effective_chat.id,
                    user_id=user.id
                )

                # Avisar al grupo
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"🚫 Usuario @{user.username} eliminado por contenido prohibido."
                )

                break

import asyncio

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, moderate))

    print("Bot iniciado...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
