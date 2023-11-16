import telebot
import requests

# Telegram bot token
TOKEN = '6917650795:AAHRGwV4VaQflMUZ8JdA-vEcuEpRHhN8xKM'

# QR code API
qrcodeapi = 'https://api.qrserver.com/v1/create-qr-code/?size=1080x1080&data='

# Create a bot instance
bot = telebot.TeleBot(TOKEN)

# Handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Please send the text for the URL.')

# Handler for text messages
@bot.message_handler(func=lambda message: True)
def text_input(message):
    text = message.text
    url = f"{qrcodeapi}{text}"
    bot.reply_to(message, url)

# Polling updates
bot.polling()
