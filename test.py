# Test File; Date 2024-01-35

import requests
import re
import stat, time ,os

#   für Seite: https://s.to (Serien..)

#   film_katalog = input("Gib ein katalog an (A-Z): ")
#   streaming_url = f"https://s.to/katalog/{film_katalog}"


# User nach Input fragen!
print("Beachte den Film Namen richtig einzugeben!")
film_name = input("Gib den Filmnamen an: ")

# LeerZeichen mit "-" replacen damit keine Suchfehler entstehen
film_name_url = film_name.replace(" ","-").replace("&", "and")
film_name_url2 = film_name.replace(" ","%20")
search_film_name = ""

# Grund Informationen Definieren
streaming_url = f"https://movies2watch.tv/search/{film_name_url.lower()}"
print(streaming_url)
pathname =f"/home/tarik/WorkSpace/Visual/Programms/telegrambot/test-movie/Film-Suche-{film_name}.txt"

# Damit "&" in der RegEx suche erkannt wird!
if "&" in film_name:
    search_film_name = film_name.replace("&", "&amp;")
 

# Download Function
def download():
    response = requests.get(streaming_url)
    if response.status_code != 200:
        print("error")
        exit
    with open(pathname, "w") as data:
        data.write(response.text)
    return response.text

# Check if File exists
if os.path.exists(pathname) == True:

#   if exsits check age  
    if ((time.time() - os.stat(pathname)[stat.ST_MTIME])>10):  # if file.txt older than 1 Hour (3600s) than:
        print("File too old redownloading")
        content = download()
    
#   if everything ok --> use it
    else:
        with open(pathname, "r") as data:
            print("File exsits, using it!")
            content = data.read()

# if not downloaded  --> download new
else:
    print("Downloading new!")
    content = download()

# Film-Suche mit RegEx (simple Lösung)
x = re.search(f"title=\"{film_name.lower()}", content.lower())
y = re.search(f"alt=\"{film_name.lower()}", content.lower())
print("x: "+x)
print("y: "+y)
if x and y == None:
    print("Film exsitiert nicht oder wurde nicht korrekt angegeben")
else: 
    print(f'Der Film "{film_name}" ist auf der Setie "{streaming_url}" verfügbar')




