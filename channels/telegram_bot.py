from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import httpx

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌱 *AgroFamíliApp*\n\n"
        "Olá! Sou seu assistente agroecológico.\n\n"
        "Posso ajudar com:\n"
        "• ATER - orientação técnica\n"
        "• Crédito - PRONAF, CAF\n"
        "• Mercado - PAA, PNAE\n"
        "• Clima - previsão do tempo\n"
        "• Documentos - regularização\n"
        "• Território - serviços locais\n\n"
        "Digite sua pergunta em texto ou envie uma mensagem de voz!",
        parse_mode="Markdown"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.message.from_user.id)

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "http://backend:8000/chat",
                json={"text": text, "user_id": user_id}
            )
            data = response.json()
            await update.message.reply_text(data.get("response", "Erro ao processar."))
    except Exception as e:
        await update.message.reply_text("Desculpe, erro de conexão. Tente novamente.")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎤 Processando áudio...")
    file = await update.message.voice.get_file()
    audio_bytes = await file.download_as_bytearray()

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "http://backend:8000/chat",
                json={"audio": audio_bytes.decode("latin-1"), "user_id": str(update.message.from_user.id)}
            )
            data = response.json()
            await update.message.reply_text(data.get("response", "Erro ao processar."))
    except Exception as e:
        await update.message.reply_text("Erro ao processar áudio.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram bot running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()