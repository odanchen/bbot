import datetime
import logging
import json
import os
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from congrator import Congrator


def get_chat_ids() -> list:
    data = json.load(open("data/chats.json"))
    return [item.get("id") for item in data]


ELIGIBLE_CHATS = get_chat_ids()  # [522982703, -388961102]
BOT_TOKEN = os.getenv("BOT_TOKEN")

print(ELIGIBLE_CHATS)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher
congrator = Congrator()


def start(update: Update, context: CallbackContext):
    logging.log(level=logging.INFO, msg=f"chat id: {update.effective_chat.id}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Target locked")


def reload(update: Update, context: CallbackContext):
    congrator.reload()


def scheduled_congrate(context: CallbackContext):
    logging.log(level=logging.INFO, msg="Daily job executed")
    messages = congrator.get_messages()
    for chat in ELIGIBLE_CHATS:
        for message in messages:
            context.bot.send_message(chat_id=chat, text=message)


# Starting daily job to notify eligible chats
# Note: in UTC Time!
updater.job_queue.run_daily(callback=scheduled_congrate, days=(0, 1, 2, 3, 4, 5, 6),
                            time=datetime.time(6, 00, 00, 000000))

# adding handlers for direct commands
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('reload', reload))

# starting bot
updater.start_polling()
updater.idle()
