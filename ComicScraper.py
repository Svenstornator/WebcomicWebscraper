import os
import sqlite3
import json
from webcomic import *

DRIVER = "ODBC Driver 17 for SQL Server"

SAVELOCATION = os.getcwd() + "\\webcomics\\"
print(SAVELOCATION)

webseries = []
restart = False
openJson = open('webcomiclist.json')
data = json.load(openJson)

for webcomic in data["webcomics"]:
    webseries.append(Webcomic(webcomic["name"], webcomic["baseURL"], webcomic["startURL"], webcomic["nextURLXPath"],
                              webcomic["comicXPath"]))

# Test if database exists first
connection = sqlite3.connect("webcomics.db")

for comic in webseries:
    print(comic.name)
    comicsToDownload = True
    saveTo = SAVELOCATION + comic.name + "/"

    if not os.path.exists(saveTo):
        os.makedirs(saveTo)

    cursor = connection.execute("SELECT * FROM webseries "
                                "WHERE webseries_name = '" + comic.name + "';")

    webseriesData = cursor.fetchone()

    if webseriesData is None:
        connection.execute("INSERT INTO webseries"
                           " (webseries_name, base_URL, latest_URL, latest_index) "
                           "VALUES ('" + comic.name + "', '" + comic.baseUrl + "', '" + comic.currentUrl + "', 1);")
        connection.commit()
        print("Added comic to database")
        indexOfComic = 1
    else:
        comic.currentUrl = webseriesData[2]
        indexOfComic = webseriesData[4]
        restart = True

    while comicsToDownload:

        print("\rDownloading comic : " + str(indexOfComic) + " " + comic.currentUrl, end='')

        try:
            comic.getComic(saveTo, indexOfComic)
            if restart is False:
                query = ("INSERT INTO webcomics_issue_locations (webseries_name, issue, issue_location)"
                         " VALUES ('" + comic.name + "', '" + str(indexOfComic) + "', '" + saveTo[1:] +
                         "\\" + str(indexOfComic).zfill(5) + ".gif" + "');")
                connection.execute(query)
            else:
                restart = False
        except IndexError:
            print("\rNo comic found at: " + comic.currentUrl + "\n")
        except HTTPError:
            connection.execute("INSERT INTO missed_comics "
                               "(webseries_id, missed_URL) "
                               "VALUES ('" + webseriesData[0] + "', '" + comic.currentUrl + "');")

        connection.execute("UPDATE webseries "
                           "SET latest_URL = '" + comic.currentUrl + "', latest_index = " + str(indexOfComic) +
                           " WHERE webseries_name = '" + comic.name + "';")

        connection.commit()
        try:
            nextPage = comic.getNext()
            if nextPage == comic.currentUrl or nextPage[-1] == '#':
                comicsToDownload = False
            else:
                comic.currentUrl = nextPage
        except Exception:
            comicsToDownload = False

        indexOfComic = indexOfComic + 1
    print("\nEnd of comic")

connection.close()
