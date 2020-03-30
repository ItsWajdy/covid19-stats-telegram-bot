import logging
import os

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from data import fetch
from reply_messages import start_message
from reply_messages import help_message
from reply_messages import error_parsing_message
from reply_messages import error_message
from reply_messages import today_response_message
from reply_messages import standby_message
from backend import get_results_today
from backend import get_results_graph


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    '''
    Respond when the command /start is issued
    '''
    fetch()
    update.message.reply_markdown(start_message)

def help(update, context):
    '''
    Respong when the command /help is issued
    '''
    fetch()
    update.message.reply_markdown(help_message)

def __parse_message(message):
    '''
    Parse input message to make sure it meets needed criteria, and extract the command after splitting the message into its 3 parts.

    Parameters:
        - message: The message passed from the user.
    
    Returns:
        - insight: The wanted insight.
        - space: The name of the country for which to get insight.
        - time: The time span through which to get insight.
    '''
    words = message.lower().split(' ')
    assert len(words) >= 4, ValueError('Message not understood')
    assert words[0] == 'total' or words[0] == 'new' or words[0] == 'active', ValueError('Insight not understood')
    assert words[1] == 'cases' or words[1] == 'deaths' or words[1] == 'recovered', ValueError('Insight not understood')
    assert words[-1] == 'today' or words[-1] == 'graph', ValueError('Time dimension not understood')

    insight = ' '.join(words[0:2])
    space = ' '.join(words[2:-1])
    time = words[-1]

    return insight, space, time

def get_insight(update, context):
    '''
    Respond to insight request by either sending a message containg today's figures, or sending an image containing a graph showing
    a certain insight number as a function of time.
    '''
    fetch()

    message = update.message.text
    try:
        insight, space, time = __parse_message(message)
    except ValueError:
        update.message.reply_markdown(error_parsing_message)
        return
    
    update.message.reply_markdown(standby_message)
    try:
        if time == 'today':
            success, result = get_results_today(insight, space, time)
        else:
            success, result = get_results_graph(insight, space, time, update.update_id)
    except ValueError:
        update.message.reply_markdown(error_parsing_message)
        return
    
    if success == 0:
        update.message.reply_markdown(error_message)
        return
    
    if time == 'today':
        if space != 'worldwide':
            space = 'in ' + space
        update.message.reply_markdown(today_response_message.format(result, insight, space))
    else:
        update.message.reply_photo(photo=open(result, 'rb'))

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
    dp.add_handler(CommandHandler('help', help))

    dp.add_handler(MessageHandler(Filters.text, get_insight))

    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
