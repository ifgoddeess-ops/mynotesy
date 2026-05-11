import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 токен берётся из Railway Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🌸 старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌸 привет\n"
        "я твой личный дневник 🩵\n\n"
        "просто пиши мне — я сохраню всё, что ты скажешь 📝"
    )

# 📝 обработка сообщений (дневник)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # 🧸 простая логика папок
    if "напомни" in text or "не забыть" in text:
        folder = "🔗🏝️ напоминания"
    elif "люблю" in text or "счаст" in text:
        folder = "🌸💌 избранное"
    elif "грусть" in text or "плохо" in text or "трев" in text:
        folder = "🧘🏼‍♀️🩵 ai режим"
    else:
        folder = "📂🧸 мои заметки"

    await update.message.reply_text(
        f"📝 сохранено в папку: {folder}\n🩵 {text}"
    )
    )

# 🚀 запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()
    def ai_reply(text: str):
    text = text.lower()

    if "грусть" in text or "плохо" in text:
        return "🫂 я рядом с тобой... всё пройдёт, правда 🩵"
    elif "люблю" in text:
        return "🌸 это очень красиво... береги это чувство"
    elif "устал" in text:
        return "🧸 отдохни немного, ты не должна всё тянуть одна"
    elif "привет" in text:
        return "🌸 приветик 🩵 я здесь"
    else:
        return "🩵 я тебя поняла... расскажи ещё"

if __name__ == "__main__":
    main()
