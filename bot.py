import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🌸 старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.chat_id)

    supabase.table("users").upsert({
        "user_id": user_id,
        "language": "ru",
        "ai_credit": 10
    }).execute()

    await update.message.reply_text("🌸 привет! я твой дневник 🩵")

# 📝 текст
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.chat_id)
    text = update.message.text

    supabase.table("notes").insert({
        "user_id": user_id,
        "text": text
    }).execute()

    await update.message.reply_text("🌸 сохранено 🩵")

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_text))

app.run_polling()
