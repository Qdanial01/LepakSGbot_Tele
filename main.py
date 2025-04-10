from typing import Final
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

#Import handle_response from bot_response.py
from response import handle_response

load_dotenv()
Bot_Token: Final[str] = os.getenv('Bot_Token')
Bot_Username: Final = '@LepakSG_Bot'

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Looking for somewhere to lepak?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Type a town and I\'ll give you a recommendation! Not sure what are the available towns? Type \'\Towns\' for a list!')

async def towns_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('These are the available towns')

#Responses prepared in response.py
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type in ['group', 'supergroup']:
        if Bot_Username in text:
            new_text: str = text.replace(Bot_Username, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str =handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(Bot_Token).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('towns', towns_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    #Polls the text (ensures previous handlers tun)
    print('Polling....')
    app.run_polling(poll_interval=3)