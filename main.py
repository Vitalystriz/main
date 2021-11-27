# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
import telebot
import sqlite3
import random
connection=sqlite3.connect("users3.db")
cursor=connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users3(
userId INTEGER PRIMARY KEY,
state INTEGER,
username TEXT)
""")
connection.commit()
state=0
name="Виталий"
token = ""
bot = telebot.TeleBot(token)
to_chat_id=0

latitude=""
longitude=""

@bot.message_handler(commands=["start"])
def send_start_message(message):
    bot.send_message(message.chat.id, "This is a bot for sending location. Write '@user:latitude;longitude' for sending.")
@bot.message_handler(commands=["recieve"])
def send_start_message(message):
    bot.send_message(message.chat.id, "for giving instruction write '/instruction'")
    global state,name
    state=1
    local_connection = sqlite3.connect("users3.db")
    local_cursor = local_connection.cursor()
    local_cursor.execute(f"INSERT INTO users3 VALUES(?,?,?);",(message.chat.id,state,message.from_user.username))
    local_connection.commit()
@bot.message_handler(content_types=["text"])
def take_message(message):
    global state, name, to_chat_id
    if get_state(message)==1:
        state = 2
        name = message.text
        local_connection = sqlite3.connect("users3.db")
        local_cursor = local_connection.cursor()
        local_connection.commit()
        msg=message.text
        for i in range (len(msg)):
            if msg.isdigit()==False and msg.isalpha()==False:
                if msg[i]==":":
                    username=msg[:i]
                    location=msg[i+1:]

        for i in range(len(location)):
            if location[i]==";":
                global latitude, longitude
                longitude = location[i + 1:]
                latitude = location[:i-1]

        local_cursor.execute(f" SELECT * from users3 ;")
        all_fetchall=local_cursor.fetchall()

        for i in range(len(all_fetchall)):
            for j in range(len(all_fetchall[i])):
                if str(all_fetchall[i][j])==username[1:]:
                    to_chat_id=all_fetchall[i][j-2]




        bot.send_location(to_chat_id, latitude=float(latitude), longitude=float(longitude), live_period=None)
        remove()

def get_state(message):
    return state
def remove():
    global to_chat_id
    to_chat_id=0

bot.polling(none_stop=True, interval=0)



