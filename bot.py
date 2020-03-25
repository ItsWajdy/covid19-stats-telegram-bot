import logging
import os

from telegram.ext import Updater
from telegram.ext import CommandHandler

from .data import fetch
from .reply_messages import __start_message


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    '''
    Respond when the command /start is issued
    '''
    fetch()
    update.message.reply_markdown(__start_message)

def error(update, context):
    '''
    Log errors caused by Updates
    '''
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    '''
    Start the bot
    '''
    fetch()

    TOKEN = os.getenv('TOKEN')
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
