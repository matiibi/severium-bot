import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ==========================
# CONFIGURACIÓN
# ==========================

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# Palabras relacionadas a drogas
PALABRAS_DROGAS = [
    "coca",
    "cocaina",
    "cristal",
    "metanfetamina",
    "tussi",
    "mdma",
    "lsd",
    "ketamina",
    "heroina",
    "vendo droga",
    "venta droga"
]

# Palabras relacionadas a contenido ilegal grave
PALABRAS_CRITICAS = [
    "cp",
    "child porn",
    "preteen",
    "minor sex",
    "13yo",
    "12yo",
    "pthc",
    "lolita"
]

# Emojis asociados a drogas
EMOJIS_PROHIBIDOS = [
    "💊",
    "❄️",
    "🧪",
    "💉"
]

# Unificamos todo
LISTA_PROHIBIDA = PALABRAS_DROGAS + PALABRAS_CRITICAS + EMOJIS_PROHIBIDOS


# ==========================
# FUNCIÓN DE MODERACIÓN
# ==========================

async def moderar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    texto = update.message.text.lower()

    for elemento in LISTA_PROHIBIDA:
        if elemento in texto:
            user_id = update.effective_user.id
            chat_id = update.effective_chat.id

            try:
                await update.message.delete()
            except:
                pass

            try:
                await context.bot.ban_chat_member(chat_id, user_id)
            except:
                pass

            logging.info(f"Usuario {user_id} eliminado por contenido prohibido.")
            break


# ==========================
# MAIN
# ==========================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, moderar)
    )

    print("Severium activo 24/7")
    app.run_polling()


if __name__ == "__main__":
    main()
