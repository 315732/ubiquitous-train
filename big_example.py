import os
import sqlite3
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


# Initialize database (create connection inside functions instead of globally)
def init_db():
    connection = sqlite3.connect("database.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS COLLECTIONS")
    cursor.execute("CREATE TABLE COLLECTIONS (BIN VARCHAR(12) NOT NULL PRIMARY KEY);")
    # Insert sample data (modify as needed)
    sample_bins = [
        ("123456789012",),
        ("987654321098",),
        ("555555555555",)
    ]
    cursor.executemany("INSERT INTO COLLECTIONS (BIN) VALUES (?)", sample_bins)
    connection.commit()
    connection.close()


init_db()  # Run database setup once


# Create Inline Keyboard
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🏠 Contact", callback_data="contact"))
    markup.add(InlineKeyboardButton("❓ Help", callback_data="help"))
    return markup

@bot.message_handler(commands=['help', 'start'])
def send_help_handler(message):
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=main_menu())







# Store temporary user data
user_data = {}

@bot.message_handler(commands=['contact'])
def send_contact_handler(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "Enter BIN:")
    bot.register_next_step_handler(message, check_bin)


def check_bin(message):
    chat_id = message.chat.id
    user_data.setdefault(chat_id, {})
    user_data[chat_id]['client_bin'] = message.text.strip()
    bot.send_message(chat_id, "Enter your message:")
    bot.register_next_step_handler(message, send_task)


def send_task(message):
    chat_id = message.chat.id
    user_data.setdefault(chat_id, {})

    client_bin = user_data[chat_id].get('client_bin', '').strip()
    client_task = message.text.strip()

    if not client_bin or not client_task:
        bot.send_message(chat_id, "Invalid input. Please try again.")
        return

    # Open a new connection per function call
    connection = sqlite3.connect("database.db", check_same_thread=False)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM COLLECTIONS WHERE BIN = ?", (client_bin,))
        result = cursor.fetchone()

        if result is None:
            bot.send_message(chat_id, "BIN not found.")
            return

        bot.send_message(chat_id, "Task created", reply_markup=main_menu())
    finally:
        cursor.close()
        connection.close()  # Always close DB connection

    user_data.pop(chat_id, None)  # Cleanup








@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "contact":
        send_contact_handler(call.message)
    elif call.data == "help":
        bot.send_message(call.message.chat.id, "Choose an option:", reply_markup=main_menu())





print("Running...")
bot.polling()
