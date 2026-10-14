import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ @muta_748_bot V3 Best Odds + Prediction RUNNING!")

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Searching: {update.message.text}")

def main():
    print("BOT @muta_748_bot RUNNING - V3 Best Odds + Prediction...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))
    app.run_polling()

if __name__=="__main__":
    main()
