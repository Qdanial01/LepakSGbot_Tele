from typing import Final
import os
from dotenv import load_dotenv
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import CallbackQueryHandler
import json

from response import handle_response

#Load towns for town command
with open('towns.json', 'r', encoding='utf-8') as file:
    towns = json.load(file)



load_dotenv()
Bot_Token: Final[str] = os.getenv('Bot_Token')
Bot_Username: Final = '@LepakSG_Bot'

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Looking for somewhere to lepak?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Type a town and I\'ll give you a recommendation! \n'
                                    'Not sure how to type? Type or select \'/example\' to see a sample! \n'
                                    'Not sure what are the available towns? Type or select \'/towns\' for a list!')

async def example_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Example 1: Random spot in town - ang mo kio \n' \
    'Example 2: A spot in town with a specific category - ang mo kio food \n' \
    'Categories: parks, malls, food')

async def towns_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(town.title(), callback_data=town)] for town in towns]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('These are the available towns:', reply_markup=reply_markup)

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

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    town_selected = query.data  # This is the town name from the button
    response = handle_response(town_selected)

    await query.edit_message_text(text=response)


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(Bot_Token).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('example', example_command))
    app.add_handler(CommandHandler('towns', towns_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Town Button
    app.add_handler(CallbackQueryHandler(button_handler))

    #Errors
    app.add_error_handler(error)

    #Polls the text (ensures previous handlers tun)
    print('Polling....')
    app.run_polling(poll_interval=3)