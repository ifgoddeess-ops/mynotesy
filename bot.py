import os
import json
import random
import datetime

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters
)

# 🔐 TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 💾 FILE MEMORY
MEMORY_FILE = "memory.json"

# 💸 CREDITS
user_credits = {}
START_CREDITS = 88

# 🧠 MEMORY
def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

memory = load_memory()


# 🤖 AI COST
AI_LIGHT_COST = 1
AI_DEEP_COST = 3


# 🧠 AI DETECT
def detect_ai_type(text: str):
    t = text.lower()
    deep_words = ["грусть", "плохо", "люблю", "устал", "одиноко", "тяжело"]

    if any(w in t for w in deep_words):
        return "deep"

    if len(t) > 40:
        return "deep"

    return "light"


# 🤖 AI REPLY
def ai_reply(text: str):
    t = text.lower()

    if "грусть" in t:
        return random.choice(["🫧 я рядом", "🫧 я с тобой"])
    elif "люблю" in t:
        return "💌 это красиво"
    elif "устал" in t:
        return "🧘🏼‍♀️ отдохни"
    elif "привет" in t:
        return "🌸 привет"
    else:
        return "🫧 я тебя поняла"


# 🌸 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)

    if user_id not in user_credits:
        user_credits[user_id] = START_CREDITS

    if user_id not in memory:
        memory[user_id] = []

    await update.message.reply_text(
        "🌸 привет\n"
        "я твой дневник 🩵\n\n"
        "🧁 нажми /menu"
    )


# 🎀 MENU
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🧁📝 новая заметка", callback_data="new_note")],
        [InlineKeyboardButton("📂🧸 мои заметки", callback_data="notes")],
        [InlineKeyboardButton("🌸💌 избранное", callback_data="fav")],
        [InlineKeyboardButton("🧘🏼‍♀️🩵 ai режим", callback_data="ai")],
        [InlineKeyboardButton("🔗🏝️ напоминания", callback_data="reminders")]
    ]

    await update.message.reply_text(
        "🧸 меню",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🧠 BUTTONS
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)

    if user_id not in memory:
        memory[user_id] = []

    data = memory[user_id]

    if query.data == "new_note":
        await query.edit_message_text("🧁📝 просто напиши сообщение")

    elif query.data == "notes":
        notes = [i["text"] for i in data[-10:]]
        await query.edit_message_text(
            "📂🧸 заметки:\n\n" + "\n".join(notes or ["пусто"])
        )

    elif query.data == "fav":
        fav = [i["text"] for i in data if "люблю" in i["text"].lower()]
        await query.edit_message_text(
            "🌸💌 избранное:\n\n" + "\n".join(fav[-10:] or ["пусто"])
        )

    elif query.data == "ai":
        ai = [i["text"] for i in data if any(x in i["text"].lower() for x in ["грусть","плохо","устал"])]
        await query.edit_message_text(
            "🧘🏼‍♀️🩵 ai режим:\n\n" + "\n".join(ai[-10:] or ["пусто"])
        )

    elif query.data == "reminders":
        rem = [i["text"] for i in data if "напомни" in i["text"].lower()]
        await query.edit_message_text(
            "🔗🏝️ напоминания:\n\n" + "\n".join(rem[-10:] or ["пусто"])
        )


# 📝 HANDLE TEXT
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    text = update.message.text
    low = text.lower()
    now = str(datetime.datetime.now())

    # 💸 init
    if user_id not in user_credits:
        user_credits[user_id] = START_CREDITS

    if user_id not in memory:
        memory[user_id] = []

    # 💸 check credits
    if user_credits[user_id] <= 0:
        await update.message.reply_text("🫧 пока нет доступа")
        return

    # 💾 save memory
    memory[user_id].append({"text": text, "date": now})
    save_memory(memory)

    # 📂 folders
    if "напомни" in low:
        folder = "🔗🏝️ напоминания"
    elif "люблю" in low:
        folder = "🌸💌 избранное"
    elif "грусть" in low or "плохо" in low:
        folder = "🧘🏼‍♀️🩵 ai режим"
    else:
        folder = "📂🧸 мои заметки"

    # 🧠 AI level
    ai_type = detect_ai_type(text)

    ai_text = "🫧 сохранено"

    cost = AI_LIGHT_COST if ai_type == "light" else AI_DEEP_COST

    if user_credits[user_id] >= cost:
        user_credits[user_id] -= cost
        ai_text = ai_reply(text)

    await update.message.reply_text(
        f"📝 сохранено\n"
        f"📂 {folder}\n\n"
        f"🫧 {ai_text}"
    )


# 🚀 RUN
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))

    app.add_handler(CallbackQueryHandler(button_handler))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()


if __name__ == "__main__":
    main()
