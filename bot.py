#!/usr/bin/env python
import logging

from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from config import APP_CONFIG
from storage import search_data, read_data

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Привіт {user.mention_markdown_v2()}\!",
        reply_markup=ForceReply(selective=True),
    )
    update.message.reply_text("Для пошуку введіть [номер/марка авто/місто] ")
    update.message.reply_text("Для списоку всіх машин")
    update.message.reply_text("/list")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Для пошуку введіть [номер/марка авто/місто] ")
    update.message.reply_text("Для списоку всіх машин")
    update.message.reply_text("/list")


def search_command(update: Update, context: CallbackContext) -> None:
    """search cars"""
    cars = search_data(update.message.text)
    if cars:
        message = "\n".join([str(c) for c in cars])
    else:
        message = "Не знайдено"
    update.message.reply_text(message)


def list_command(update: Update, context: CallbackContext) -> None:
    """list all cars"""
    cars = read_data()
    if cars:
        message = "\n\n".join([str(c) for c in cars])
    else:
        message = "Не знайдено"
    update.message.reply_text(message)


def main() -> None:
    """Start the bot."""
    updater = Updater(APP_CONFIG["TELEGRAM_TOKEN"])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("list", list_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, search_command)
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
