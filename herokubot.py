import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import requests
from bs4 import BeautifulSoup


def bowls(bot, update):
    resp = requests.get('https://myfunkybowl.com/collections/bowls')
    soup = BeautifulSoup(resp.text, 'html.parser')
    all_bowls = soup.find_all('span', class_='grid-product__title')
    # date_title = soup.find('header', class_='section-header text-center')

    for bowl in all_bowls:
        update.effective_message.reply_text('🥗 ' + bowl.text.strip())


def echo(bot, update):
    update.effective_message.reply_text(update.effective_message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == "__main__":
    # Set these variable to the appropriate values

    TOKEN = os.environ.get('MYFUNKYBOT_API')
    NAME = os.environ.get('APP_NAME') or 'myfunkybot'

    # Port is given by Heroku
    PORT = os.environ.get('PORT') or 8843

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('bowls', bowls))
    dp.add_error_handler(error)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
