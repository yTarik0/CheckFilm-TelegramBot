import requests
import re
import stat, time ,os

#   für Seite: https://s.to (Serien..)

#   film_katalog = input("Gib ein katalog an (A-Z): ")
#   streaming_url = f"https://s.to/katalog/{film_katalog}"

print("Beachte den Film Namen richtig einzugeben!")
film_name = input("Gib den Filmnamen an: ")

# LeerZeichen mit "-" replacen damit keine Suchfehler entstehen
film_name_url = film_name.replace(" ","-")
streaming_url = f"https://dopebox.to/search/{film_name_url}"

pathname =f"/home/tarik/WorkSpace/Visual/Programms/telegrambot/Dopebox.to/Film-Suche-{film_name}.txt"

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

    # if exsits check age  
    if ((time.time() - os.stat(pathname)[stat.ST_MTIME])>10):  # if file.txt older than 1 Hour (3600s) than:
        print("File too old redownloading")
        content = download()
    
    else:
        with open(pathname, "r") as data:
            print("File exsits, using it!")
            content = data.read()

# if not downloaded 
else:
    print("Downloading new!")
    content = download()

# Film-Suche mit RegEx (simple Lösung)
x = re.search(f"title=\"{film_name}", content)
if x == None:
    print("Film exsitiert nicht oder wurde nicht korrekt angegeben")
else: 
    print(f'Der Film "{film_name}" ist auf der Setie "{streaming_url}" verfügbar')




