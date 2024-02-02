# telegrambBot.py --> checkMovie telegramBot 2024-02-01

# imports --> libary
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from checkMovie import main
import time

load_dotenv()

commandlist = ["/commandlist", "/checkmovie","/usage",]

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)
bot = telebot.TeleBot(API_KEY)
print("🛫 Telegram-Bot: CheckMovie is running...🛫")

# Commandlist Command
@bot.message_handler(commands=["commandlist"])
def get_commmandlist(message):
    commands_str = "\n".join(commandlist)
    bot.reply_to(message, f"<b>Available Commands</b>:\n{commands_str}",  parse_mode='HTML')

# Check Movie Command
@bot.message_handler(commands=["checkmovie"])
def checkMovie(message):
    parts = message.text.split()
    if len(parts) > 1:
        film_name = ' '.join(parts[1:])
        bot.reply_to(message, f"Checking where Movie - <b>{film_name.upper()}</b> available", parse_mode='HTML')
        
        result = main(film_name)
        time.sleep(5)
        bot.reply_to(message,result, parse_mode='HTML')
    else:
        bot.reply_to(message, "Please enter a Movie-Name after the Command")

# Usage Command
@bot.message_handler(commands=["usage"])
def usage(message):
    bot.reply_to(message, "Usage: Use /checkmovie [movie-name] to search for a movie's availability.\nPlease make sure you make no mistake when typing the movie name")


# Auto Response if text-message is not a Command
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_all( message):
    local_command_list = ["/hello", "/checkmovie", "/usage", "/commandlist"]
    is_command = any(message.text.startswith(command) for command in local_command_list)
    if not is_command:
        # Inline-Keyboard erstellen
        markup = InlineKeyboardMarkup()
       
            
        # Button der über die gesamte Breite geht
        search_button = InlineKeyboardButton("🔎 Search for a Movie", callback_data='search_button')
        markup.add(search_button)  # Fügt den Button in seiner eigenen Reihe hinzu
            
        #  Buttons nebeneinander in einer neuen Reihe
        usage_button = InlineKeyboardButton("❔ Usage", callback_data='usage_button')
        close_button = InlineKeyboardButton("❌ Close", callback_data='close_button')
            
        markup.row(usage_button, close_button)  # Fügt beide Buttons in der gleichen Reihe hinzu

        support_button = InlineKeyboardButton("📥 Contact-Support", callback_data='support_button')
        markup.add(support_button)

        # User Pingen!
        user_first_name = message.from_user.first_name
        mention = f'<a href="tg://user?id={message.from_user.id}">{user_first_name}</a>'
            
        # Nachricht mit Inline-Keyboard senden
        bot.reply_to(message, f"<b>Hello {mention}</b> 👋,\nPlease run one of the <b>Commands</b> by clicking on the buttons or by typing <b>/commandlist</b> in the chat\nto get a <b>list of all commands</b>", reply_markup=markup, parse_mode='HTML')


# Button-Callbacks --> if button pressed:
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "usage_button":
        # Benachrichtigung Oben Response Pop-Up
        bot.answer_callback_query(call.id, "Usage: Use /checkmovie [movie-name] to search for a movie's availability.")
        # Text-Message Response
        bot.send_message(call.message.chat.id, "Usage: Use /checkmovie [movie-name] to search for a movie's availability.\nPlease make sure you make no mistakes when typing the movie name")

    if call.data == "search_button":
       forceReply_markUp = telebot.types.ForceReply(selective=True)
       bot.send_message(call.message.chat.id, "Please type the movie name", reply_markup=forceReply_markUp)
       bot.answer_callback_query(call.id)

    if call.data == "support_button":
        bot.answer_callback_query(call.id, "CheckMovieSOL")
        bot.send_message(call.message.chat.id, "CheckMovieSOL")

# Am Ende des Codes damit alle Befehle gesynced sind
bot.polling(none_stop=True) # none_stop=True --> wenn fehler kommt damit nicht stopt