from telegram import Update #contains information about the incoming message
from telegram.ext import ContextTypes,CommandHandler #tools to handle the message


#this function is called when the /start command is received
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Hello {user.first_name}! I'm your bot. How can I help you today?")


def register_handlers(application):
    application.add_handler(CommandHandler("start", start))
    print("start command handler registered")













