from telegramBot import bot
from logsNotification import notify_logsUpdate

def run():
    try:
        # Bot Starting....
        print("🛫 Telegram-Bot: CheckMovie is running...🛫")
        bot.polling(none_stop=True) # none_stop=True --> wenn fehler kommt damit nicht stopt
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    run()
    notify_logsUpdate()
    
