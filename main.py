import os
import requests
from bs4 import BeautifulSoup
import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Initialize the Telegram bot API with your bot token
bot = telegram.Bot(token=os.environ['6233078024:AAF07bwJh0s-aTPZIAc9I01-GXLAT1dphNM'])
updater = Updater(token=os.environ['6233078024:AAF07bwJh0s-aTPZIAc9I01-GXLAT1dphNM'])

# Specify the URL of the Telegram channel you want to parse
channel_url = 'https://t.me/VeoliaJur'

# Specify the word you want to search for in the news
search_word = 'վթարային'

# Define a handler function for incoming messages
def message_handler(update, context):
    # Send a request to the Telegram channel URL and get the HTML content
    response = requests.get(channel_url)
    html_content = response.content

    # Parse the HTML content with BeautifulSoup to extract the news items
    soup = BeautifulSoup(html_content, 'html.parser')
    news_items = soup.find_all('div', {'class': 'tgme_widget_message_bubble'})

    # Loop through the news items and check if they contain the search word
    for news_item in news_items:
        news_text = news_item.get_text()
        if search_word in news_text.lower():
            # If the news contains the search word, send it to all users who have interacted with the bot
            users = context.bot_data.get('users', set())
            for user in users:
                context.bot.send_message(chat_id=user, text=news_text)

# Define a handler function for errors
def error_handler(update, context):
    print(f'Error: {context.error}')

# Add the handlers to the updater
updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
updater.dispatcher.add_error_handler(error_handler)

# Start the bot and keep it running
updater.start_polling()

# Store the chat IDs of all users who have ever interacted with the bot in the bot's bot_data
for update in bot.get_updates():
    user = update.message.chat_id
    bot_data = updater.bot_data
    users = bot_data.get('users', set())
    users.add(user)
    bot_data['users'] = users

updater.idle()

