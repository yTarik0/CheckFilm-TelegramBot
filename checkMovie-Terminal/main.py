# Main.py File - checkMovie; Date 2024-01-35
#   --> checkMovie just per Terminal

import requests  # ---> for requests of the page
import re  # --> for RegEx
import stat, time, os  # ---> for Time, checking file - age
import urllib.parse    # ---> for parsing url

# -----------------------------------------------------------
# Für Serien: https://s.to (Seite für Serien..)

# film_katalog = input("Gib ein katalog an (A-Z): ")
# streaming_url = f"https://s.to/katalog/{film_katalog}"
# -----------------------------------------------------------

# User nach Input fragen!
print("Beachte den Film Namen richtig einzugeben!")
film_name = input("Gib den Filmnamen an: ")

# LeerZeichen mit "-" replacen damit keine Suchfehler entstehen
film_name_url = film_name.replace(" ", "-").replace("&", "and")

# LeerZeichen in HTML - Link formatieren zu "%20"  damit keine Suchfehler entstehen
film_name_url2 = film_name.replace(" ", "%20")

# WebServices to Check if Movie avaliable (10 Websites+)
url_list = [
    "https://zoechip.cc/search/",
    "https://dopebox.to/search/",
    "https://9movies.top/search/",
    "https://movies2watch.tv/search/",
    "https://myflixer.is/search/",
    "https://ww2.123moviesfree.net/search/?q=",
    "https://cineb.rs/search/",
    "https://movieroom.xyz/?s=",
    "https://netfilm.app/search?keyword=",
    "https://goku.sx/search?keyword=",
    "https://cinego.tv/search?keyword=",
    "https://flixhd.cc/search/",
    "https://movie4kto.net/search/",
    "https://hurawatch.bz/filter?keyword=",
    "https://moviesjoy.is/search/",
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
    with open(pathname, "w") as data:
        data.write(response.text)
    return response.text


# checkCache Funktion
def checkCache(streaming_url):
    # Streaming-URL Parsen ohne "https://"
    site = urllib.parse.urlsplit(streaming_url).hostname
    pathname = f"/movie-search/{site}-{film_name}.txt"
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
            with open(pathname, "r") as data:
                #               Debug Control
                # print("File exsits, using it!")
                content = data.read()

    # if not downloaded  --> download new
    else:
        # Debug Control
        # print("Downloading new!")
        content = download(pathname ,streaming_url)

    return content


# main Funktion --> hauptfunkiton
def main():
    for streaming_url in url_list:
        if streaming_url in list_2:
            streaming_url = f"{streaming_url}{film_name_url2 }"

        # Debug Control
        # print(f"STREAMING URL----: {streaming_url}")
        else:
            streaming_url = f"{streaming_url}{film_name_url}"

        search_film_name = film_name

        # Damit "&" in der RegEx suche erkannt wird!
        if "&" in film_name:
            search_film_name = film_name.replace("&", "&amp;")

        # Film-Suche mit RegEx (simple Lösung)
        x = re.search(
            f'title="{search_film_name.lower()}', checkCache(streaming_url).lower()
        )
        y = re.search(
            f'alt="{search_film_name.lower()}', checkCache(streaming_url).lower()
        )
        if x is None and y is None:  # or use --> if x and y == None:
            print(
                f'Der Film exsitiert  nicht auf der Seite "{streaming_url}" oder wurde nicht korrekt angegeben'
            )

        else:
            print(
                f'Der Film "{film_name}" ist auf der Seite "{streaming_url}" verfügbar'
            )

        checkCache(streaming_url)
        # If Web Service doesnt have the Movie delete File
        site = urllib.parse.urlsplit(streaming_url).hostname
        os.remove(f"movie-search/{site}-{film_name}.txt")
if __name__ == "__main__":
    main()