# telegrambBot.py --> checkMovie telegramBot 2024-02-01

# imports --> libary
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from checkMovie import main
import time


load_dotenv()

# Api-Key Definieren von .env file
API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

# commandliste setzten ---> auto response
commandlist = ["/checkmovie","/help","/send_logo", "/menu"]

# Ein Dictionary, um den Zustand jedes Benutzers zu speichern
user_expected_input = {}

# create list from every Message-ID --> to clear chat
message_ids = []

# add messages to List 
def add_message_id(message_id):
    message_ids.append(message_id)


# function Menu UI
def menu(message):
     # Inline-Keyboard erstellen
        markup = InlineKeyboardMarkup()
       
        # Button der über die gesamte Breite geht
        search_button = InlineKeyboardButton("🔎 Search for a Movie", callback_data='search_button')
        markup.add(search_button)  # Fügt den Button in seiner eigenen Reihe hinzu
            
        #  Buttons nebeneinander in einer neuen Reihe
        usage_button = InlineKeyboardButton("❔ Usage", callback_data='usage_button')
        close_button = InlineKeyboardButton("❌ Clear Chat", callback_data='clear_button')
            
        markup.row(usage_button, close_button)  # Fügt beide Buttons in der gleichen Reihe hinzu

        support_button = InlineKeyboardButton("📥 Contact-Support", callback_data='support_button')
        markup.add(support_button)

        # User Pingen!
        user_first_name = message.from_user.first_name
        user_name = f'<a href="tg://user?id={message.from_user.id}">{user_first_name}</a>'
            
        # Nachricht mit Inline-Keyboard senden
        reply = bot.reply_to(message, f"<b>Hello {user_name}</b> 👋,\nPlease do one of the Actions by <b>clicking on the Buttons</b> or by typing <b>/help</b> in the chat", reply_markup=markup, parse_mode='HTML')
        add_message_id(reply.message_id)

        
# Check-Movie Commannd --> funcitons:

# function checkMovie
def checkMovie(message):
    user_expected_input[message.chat.id] = True
    reply = bot.reply_to(message, "Please type a movie name")
    add_message_id(reply.message_id)


# function message handler --> respond like telegrambot
@bot.message_handler(func=lambda message: message.chat.id in user_expected_input)
def handle_movie_name(message):
   
    # Define Variablen für --> Movie Search Logs
    film_name = message.text
    usrname = message.from_user.username
    usr_nickname = message.from_user.first_name
    logs_file = "C:/Users/tarik/OneDrive/Desktop/Home/Users/Tarik/Coding/Workspace/CheckFilm-TelegramBot-main/app/logs/user_Search_logs.txt"


    if user_expected_input.pop(message.chat.id, None):
        # Print User Search
        print(f'🔎 Telegram-User: "{usrname}" called "{usr_nickname}" looked for the Movie "{film_name}", At Time: {time.strftime("%d.%m.%Y %H:%M:%S")} 🔎')
    
        # # Save Data in Logs
        with open(logs_file, "a+", encoding='utf-8') as data:
            data.write(f'Telegram-User: "{usrname}" called "{usr_nickname}" looked for the Movie "{film_name}", At Time: {time.strftime("%d.%m.%Y %H:%M:%S")}\n')


        result = main(film_name)
        markup = InlineKeyboardMarkup()
        menu_button = InlineKeyboardButton("📊 Back to Menu", callback_data='menu_button')

        search_again_button = InlineKeyboardButton("🔎 Search again", callback_data='search_again')

        markup.add(menu_button)
        markup.add(search_again_button)

        reply = bot.reply_to(message, result, reply_markup=markup, parse_mode='HTML', disable_web_page_preview=True)
        add_message_id(reply.message_id)

# checkMovie Command
@bot.message_handler(commands=["checkmovie"])
def command_handler(message):
    checkMovie(message)


# /menu command
@bot.message_handler(commands=["menu"])
def send_menu(message):
    menu(message)


# Test Command ---> send picture in chat
@bot.message_handler(commands=["send_logo"])
def get_logo(message):
    bot.send_photo(chat_id=message.chat.id, photo=open('app/bot-data/bot-logo.jpg', 'rb'), caption='<b>Thats the CheckMovie-Bot Logo</b>', parse_mode='HTML')

# Usage Command
@bot.message_handler(commands=["help"])
def usage(message):
    bot.reply_to(message, "<b>Movie-Search Usage:</b>\nType <b>/checkmovie</b> & after the Bot-Response\nthe <b>[movie name]</b> to start your search\nPlease make sure you make <b>no mistakes</b> when typing the movie name", parse_mode='HTML')


# Auto Response if text-message is not a Command
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_all( message):
    local_command_list = ["/help", "/checkmovie","/send_logo", "/menu"]
    is_command = any(message.text.startswith(command) for command in local_command_list)
    if not is_command:
        menu(message)

       
# Button-Callbacks --> if button pressed:
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    # Define Data ---> for logs
    usrname = call.from_user.username
    usr_nickname = call.from_user.first_name
    logs_file = "C:/Users/tarik/OneDrive/Desktop/Home/Users/Tarik/Coding/Workspace/CheckFilm-TelegramBot-main/app/logs/button_logs.txt"

    if call.data == "usage_button":
        # Save Data in Logs
        with open(logs_file, "a+", encoding='utf-8') as data:
            data.write(f'Telegram-User: "{usrname}" called "{usr_nickname}" pressed the Usage-Button, At Time: {time.strftime("%d.%m.%Y %H:%M:%S")}\n')

        # Benachrichtigung Oben Response Pop-Up
        bot.answer_callback_query(call.id, "Usage: Use /checkmovie [movie-name] to search for a movie's availability.")
        reply = bot.send_message(call.message.chat.id, "Usage: Use /checkmovie [movie-name] to search for a movie's availability.\nPlease make sure you make no mistakes when typing the movie name")
        add_message_id(reply.message_id)

    if call.data == "search_button":
       # Save Data in Logs
       with open(logs_file, "a+", encoding='utf-8') as data:
            data.write(f'Telegram-User: "{usrname}" called "{usr_nickname}" pressed the Search-Button, At Time: {time.strftime("%d.%m.%Y %H:%M:%S")}\n')

       bot.answer_callback_query(call.id,"Type a Movie Name in the Chat")
       checkMovie(call.message)

    if call.data == "search_again":
        # Save Data in Logs
        with open(logs_file, "a+", encoding='utf-8') as data:
            data.write(f'Telegram-User: "{usrname}" called "{usr_nickname}" pressed the Search-Button, At Time: {time.strftime("%d.%m.%Y %H:%M:%S")}\n')


        bot.answer_callback_query(call.id,"Type a Movie Name in the Chat")
        checkMovie(call.message)
       
    if call.data == "support_button":
        # Save Data in Logs
        with open(logs_file, "a+", encoding='utf-8') as data:
            data.write(f'Telegram-User: "{usrname}" called "{usr_nickname}" pressed the Support-Button, At Time: {time.strftime("%d.%m.%Y %H:%M:%S")}\n')

        bot.answer_callback_query(call.id, "Contact CheckMovieSOL on Twitter")
        reply = bot.send_message(call.message.chat.id, "If there are any problems let us know\n📧 Contact: https://twitter.com/CheckMovieSOL")
        add_message_id(reply.message_id)

    if call.data == "clear_button":
        # Save Data in Logs
        with open(logs_file, "a+", encoding='utf-8') as data:
            data.write(f'Telegram-User: "{usrname}" called "{usr_nickname}" pressed the Clear-Button, At Time: {time.strftime("%d.%m.%Y %H:%M:%S")}\n')

        bot.answer_callback_query(call.id, "Chat successfully cleared!")
        for message_id in message_ids:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
            except Exception as e:
                # Debug if error
                print(f"Fehler beim Löschen der Nachricht {message_id}: {e}")
                 
        # clear list after, chat cleared!
        message_ids.clear()

    if call.data == "menu_button":
        # Save Data in Logs
        with open(logs_file, "a+", encoding='utf-8') as data:
            data.write(f'Telegram-User: "{usrname}" called "{usr_nickname}" pressed the Data-Button, At Time: {time.strftime("%d.%m.%Y %H:%M:%S")}\n')
        echo_all(call.message)

 
