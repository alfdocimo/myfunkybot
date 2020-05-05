import logging
import os
import re

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import requests

from bs4 import BeautifulSoup


def bowls(bot, update):
    resp = requests.get('https://myfunkybowl.com/collections/bowls')
    soup = BeautifulSoup(resp.text, 'lxml')

    parsed_bowls_list = []

    for bowl in soup.find_all('div', class_='grid-product__wrapper'):
        title = bowl.find('span', class_='grid-product__title')
        cta = bowl.find('a', class_='grid-product__image-link')
        cta = 'https://myfunkybowl.com/'+cta.attrs['href']

        price = bowl.find('span', class_='grid-product__price')
        available = bowl.find('div', class_='grid-product__sold-out')
        if(available):
            available = '✅ disponible'
        else:
            available = '❌ agotado'

        parse_price = re.search('€(.*?)$', price.text.strip())

        parsed_bowls_list.append(
            '🥗 ' + title.text.strip() + ' '+parse_price[0] + ' '+available + ' 👉 ' + cta + ' 👈'+'\n')

    clean_data = '\n'.join(parsed_bowls_list)

    update.effective_message.reply_text(clean_data)


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
