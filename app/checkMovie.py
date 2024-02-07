# CheckMovie.py File - checkMovie ---> file for telebot; Date 2024-02-01

# RUN telegramBot.py --> for telegrambot 

import requests  # ---> for requests of the page
import re  # --> for RegEx
import stat, time, os  # ---> for Time, checking file - age
import urllib.parse    # ---> for parsing url

# WebServices to Check if Movie avaliable (10 Websites+)
url_list = [
    "https://zoechip.cc/search/",
    "https://dopebox.to/search/",
    "https://ww2.123moviesfree.net/search/?q=",
    "https://movieroom.xyz/?s=",
    "https://netfilm.app/search?keyword=",
    "https://goku.sx/search?keyword=",
    "https://cinego.tv/search?keyword=",
    "https://hurawatch.bz/filter?keyword=",
    "https://heymovies.to/filter?keyword=",
    "https://fmoviesz.to/filter?keyword=",
    "https://ww.yesmovies.ag/search.html?q=",
    "https://primeflix-web.vercel.app/search/",
    "https://themoviearchive.site/search?query=",
    "https://watch.streamflix.one/movie?search="
]

list_2 = [
    "https://netfilm.app/search?keyword=",
    "https://movieroom.xyz/?s=",
    "https://goku.sx/search?keyword=",
    "https://cinego.tv/search?keyword=",
    "https://heymovies.to/filter?keyword=",
    "https://hurawatch.bz/filter?keyword=",
    "https://fmoviesz.to/filter?keyword=",
    "https://ww.yesmovies.ag/search.html?q=",
    "https://themoviearchive.site/search?query=",
    "https://watch.streamflix.one/movie?search="
]

# Funktionen Definieren:

# Download Funktion
def download(pathname, streaming_url):
    response = requests.get(streaming_url)
    if response.status_code != 200:
        # Debug Control
        # print("error")
        exit
    with open(pathname, "w", encoding='utf-8') as data:
        data.write(response.text)
    return response.text


# checkCache Funktion
def checkCache(streaming_url, film_name):
    # Streaming-URL Parsen ohne "https://"
    site = urllib.parse.urlsplit(streaming_url).hostname

    #pathname = (f"YOUR-PATH/movie-search/{site}-{film_name}.txt")
    pathname = f"C:/Users/tarik/OneDrive/Desktop/Home/Users/Tarik/Coding/Workspace/CheckFilm-TelegramBot-main/app/movie-search/{site}-{film_name}.txt"
    # Check if File exists
    if os.path.exists(pathname) == True:
        #   if exsits check age
        if (
            time.time() - os.stat(pathname)[stat.ST_MTIME]
        ) > 3600:  # if file.txt older than 1 Hour (3600s) than:
            # Debug Control
            # print("File too old redownloading")
            content = download(pathname, streaming_url)

        #   if everything ok --> use it
        else:
           with open(pathname, "r", encoding='utf-8', errors='replace') as data:
                #  Debug Control
                # print("File exsits, using it!")
                content = data.read()

    # if not downloaded  --> download new
    else:
        # Debug Control
        # print("Downloading new!")
        content = download(pathname ,streaming_url)

    return content


# main Funktion --> hauptfunkiton
def main(film_name):
    ergebnisse = [] 

    # LeerZeichen mit "-" replacen damit keine Suchfehler entstehen
    film_name_url = film_name.replace(" ", "-").replace("&", "and")

    # LeerZeichen in HTML - Link formatieren zu "%20"  damit keine Suchfehler entstehen
    film_name_url2 = film_name.replace(" ", "%20")

    for streaming_url in url_list:
        if streaming_url in list_2:
            streaming_url = f"{streaming_url}{film_name_url2 }"
        else:
            streaming_url = f"{streaming_url}{film_name_url}"

        search_film_name = film_name
        # Damit "&" in der RegEx suche erkannt wird!
        if "&" in film_name:
            search_film_name = film_name.replace("&", "&amp;")

        # Film-Suche mit RegEx (simple Lösung)
        x = re.search(
            f'title="{search_film_name.lower()}', checkCache(streaming_url, film_name).lower()
        )
        y = re.search(
            f'alt="{search_film_name.lower()}', checkCache(streaming_url, film_name).lower()
        )
        if x is None and y is None:  # or use --> if x and y == None:
            checkCache(streaming_url, film_name)

            # If Web Service doesnt have the Movie delete Film
            site = urllib.parse.urlsplit(streaming_url).hostname
            
            # os.remove (f"YOUR-PATH/movie-search/{site}-{film_name}.txt")
            os.remove(f"C:/Users/tarik/OneDrive/Desktop/Home/Users/Tarik/Coding/Workspace/CheckFilm-TelegramBot-main/app/movie-search/{site}-{film_name}.txt")
            
            # If you want to print out Web-Services that dont support the movie
            #ergebnisse.append(f'Movie <b>{film_name.upper()}</b> is not available on: <a href="{streaming_url}">{site}</a> ❌\n')
        else:
            site = urllib.parse.urlsplit(streaming_url).hostname
            checkCache(streaming_url, film_name)
            ergebnisse.append(f'Movie <b>{film_name.upper()}</b> is available on: <a href="{streaming_url}">{site}</a> ✅\n')

    ergebnis_string = '\n'.join(ergebnisse)
    return ergebnis_string

