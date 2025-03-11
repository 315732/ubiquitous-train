from telethon.sync import TelegramClient
import sqlite3

API_ID = ""
API_HASH = ""
GROUP_ID =   # Replace with your group ID
USER_ID =   # Replace with your user ID

# Initialize database
conn = sqlite3.connect("messages.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS sent_messages (message_id INTEGER PRIMARY KEY)")
conn.commit()

# Initialize Telegram client (User authentication)
client = TelegramClient("user_session", API_ID, API_HASH)

def get_sent_messages():
    """Retrieve the list of sent message IDs from the database."""
    cursor.execute("SELECT message_id FROM sent_messages")
    return {row[0] for row in cursor.fetchall()}

def save_sent_message(message_id):
    """Store the sent message ID in the database."""
    cursor.execute("INSERT INTO sent_messages (message_id) VALUES (?)", (message_id,))
    conn.commit()

async def forward_new_messages():
    """Fetch messages from group, check for duplicates, and send new ones to the user."""
    sent_messages = get_sent_messages()  # Get already sent messages

    async for message in client.iter_messages(GROUP_ID):
        if message.id not in sent_messages:
            try:
                await client.send_message(USER_ID, "Hello: " + message.text)  # Forward message
                save_sent_message(message.id)  # Store message ID
                print(f"Sent message: {message.id}")
            except Exception as e:
                print(f"Error sending message {message.id}: {e}")

async def main():
    await client.start()  # Login as a user
    await forward_new_messages()

with client:
    client.loop.run_until_complete(main())

# Close database connection
conn.close()
