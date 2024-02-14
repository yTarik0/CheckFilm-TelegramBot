import os
import time

# Define the path 
search_logs = 'C:/Users/tarik/OneDrive/Desktop/Home/Users/Tarik/Coding/Workspace/CheckFilm-TelegramBot-main/app/logs/user_Search_logs.txt'
button_logs = 'C:/Users/tarik/OneDrive/Desktop/Home/Users/Tarik/Coding/Workspace/CheckFilm-TelegramBot-main/app/logs/button_logs.txt'

def get_file_size(path):
    return os.path.getsize(path)

# Get last size of the file
searchLogs_last_Size = get_file_size(search_logs)
buttonLogs_last_Size = get_file_size(button_logs)
print(searchLogs_last_Size)


def notify_logsUpdate():
    while True:
        # Get Current file size
        searchLogs_Current_Size = get_file_size(search_logs)
        print(searchLogs_Current_Size)
        buttonLogs_Current_Size = get_file_size(button_logs)

        # Compare it to last size
        if searchLogs_Current_Size != searchLogs_last_Size:
            print("Check Button Logs, They got Updated!")
            buttonLogs_last_Size = buttonLogs_Current_Size

        
        if buttonLogs_Current_Size != buttonLogs_last_Size:
            print("Check Button Logs, They got Updated!")
            buttonLogs_last_Size = buttonLogs_Current_Size
