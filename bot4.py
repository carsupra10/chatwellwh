import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Telegram bot token
TOKEN = '6917650795:AAHRGwV4VaQflMUZ8JdA-vEcuEpRHhN8xKM'

#qrcode api
qrcodeapi = 'https://api.qrserver.com/v1/create-qr-code/?size=1080x1080&data='
def start(update, context):
    update.message.reply_text('Please send the text for the URL.')

# Define a function to handle text messages
def text_input(update, context):
    text = update.message.text  # Get the text sent by the user
    # Assuming you want to create a URL with the user text
    url = f"[{qrcodeapi}{text}]"
    update.message.reply_text(f'{url}')

    
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handler to trigger QR code generation
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_input))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
