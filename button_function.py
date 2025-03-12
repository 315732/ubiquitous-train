import os
import telebot
from dotenv import load_dotenv
from telebot import types

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set. Please provide your bot token.")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['help'])
def send_help(message):
    # This function now handles both the initial help command and callback queries
    if hasattr(message, 'data'):  # This is a callback query
        call = message
        if call.data == 'option1':
            bot.answer_callback_query(call.id, "You selected Option 1!")
            bot.send_message(call.message.chat.id, "You clicked Option 1")
        elif call.data == 'option2':
            bot.answer_callback_query(call.id, "You selected Option 2!")
            bot.send_message(call.message.chat.id, "You clicked Option 2")
        elif call.data == 'option3':
            bot.answer_callback_query(call.id, "You selected Option 3!")
            bot.send_message(call.message.chat.id, "You clicked Option 3")
        elif call.data == 'option4':
            bot.answer_callback_query(call.id, "You selected Option 4!")
            bot.send_message(call.message.chat.id, "You clicked Option 4")
    else:  # This is a regular command
        help_text = (
            "Available commands:\n"
            "/help - Show this help message\n"
            "You can also interact using the buttons below."
        )
        bot.send_message(message.chat.id, help_text)
        markup = types.InlineKeyboardMarkup(row_width=2)
        # Create inline buttons with callbacks
        button1 = types.InlineKeyboardButton('Option 1', callback_data='option1')
        button2 = types.InlineKeyboardButton('Option 2', callback_data='option2')
        button3 = types.InlineKeyboardButton('Option 3', callback_data='option3')
        button4 = types.InlineKeyboardButton('Option 4', callback_data='option4')
        # Add buttons to the keyboard
        markup.add(button1, button2, button3, button4)
        # Send message with inline keyboard
        bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)


# Register this same function as the callback handler
bot.callback_query_handler(func=lambda call: True)(send_help)


print("Bot is running...")
bot.infinity_polling()
