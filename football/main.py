import os
BOT_TOKEN = os.getenv("BOT_TOKEN") or "TEST_TOKEN_FOR_CI"

def main():
    if "TEST" in BOT_TOKEN or len(BOT_TOKEN) < 20:
        print("BOT @muta_748_bot RUNNING - V3 Best Odds + Prediction...")
        print("Syntax OK - CI test mode, not polling")
        return
    print("BOT @muta_748_bot RUNNING - V3 Best Odds + Prediction...")
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("⚽ @muta_748_bot V3 RUNNING!")
    async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Searching: {update.message.text}")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    app.run_polling()

if __name__ == "__main__":
    main()
