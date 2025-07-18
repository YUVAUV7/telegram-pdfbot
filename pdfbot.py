import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from thefuzz import fuzz

# 📚 Your PDF library (expand this as needed)
PDF_LIBRARY = {
    "class 10 maths": "https://ncert.nic.in/textbook/pdf/jemh1cc.pdf",
    "class 10 science": "https://ncert.nic.in/textbook/pdf/jesc1cc.pdf",
    "indian constitution": "https://legislative.gov.in/textbook/pdf/leph1cc.pdf"
}

# 🟢 /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Welcome to PDF eBook Bot!\n\n"
        "Type the name of a book (e.g., *class 10 science*) or use:\n"
        "`/search class 10 science`\n\n"
        "I’ll try to find the closest matching NCERT/public domain PDF. 📖",
        parse_mode='Markdown'
    )

# 🔍 Search handler (supports both /search and normal messages)
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if text.startswith("/search"):
        parts = text.split(" ", 1)
        if len(parts) < 2:
            await update.message.reply_text("⚠️ Please add the book name after /search.")
            return
        query = parts[1]
    else:
        query = text

    # 🔎 Fuzzy matching for similar terms
    best_match = None
    best_score = 0

    for title, link in PDF_LIBRARY.items():
        score = fuzz.partial_ratio(query, title)
        if score > best_score:
            best_match = (title, link)
            best_score = score

    if best_score > 70:  # Threshold for match confidence
        await update.message.reply_text(f"✅ Found: *{best_match[0]}*\n📥 {best_match[1]}", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ No PDF found. Try another book name.")

# 🤖 Setup the bot application
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

# 🧠 Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

print("🤖 Bot is running 24/7...")
app.run_polling()
