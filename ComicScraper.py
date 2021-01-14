import os
import pyodbc
import json
from webcomic import *

DRIVER = "SQL Server"
SERVER = ""
DATABASE = ""
USER = ""

SAVELOCATION = ".\\webcomics\\"

webseries = []
restart = False
openJson = open('webcomiclist')
data = json.load(openJson)

for webcomic in data["webcomics"]:
    webseries.append(Webcomic(webcomic["name"], webcomic["baseURL"], webcomic["startURL"], webcomic["nextURLXPath"],
                              webcomic["comicXPath"]))


connection = pyodbc.connect("driver=" + DRIVER
                            + ";server=" + SERVER
                            + ";user=" + USER
                            + ";database=" + DATABASE + ";")
cursor = connection.cursor()

for comic in webseries:
    print(comic.name)
    comicsToDownload = True
    saveTo = SAVELOCATION + comic.name + "\\"

    if not os.path.exists(saveTo):
        os.makedirs(saveTo)

    cursor.execute("SELECT * FROM webseries "
                   "WHERE webseries_name = '" + comic.name + "';")
    webseriesData = cursor.fetchone()

    if webseriesData is None:
        cursor.execute("INSERT INTO webseries"
                       " (webseries_name, base_URL, latest_URL, latest_index) "
                       "VALUES ('" + comic.name + "', '" + comic.baseUrl + "', '" + comic.currentUrl + "', 1);")
        connection.commit()
        print("Added comic to database")
        indexOfComic = 1
    else:
        comic.currentUrl = webseriesData[3]
        indexOfComic = webseriesData[5]
        restart = True

    while comicsToDownload:

        print("\rDownloading comic : " + str(indexOfComic), end='')

        try:
            comic.getComic(saveTo, indexOfComic)
            if restart is False:
                cursor.execute("INSERT INTO webcomics_issue_locations"
                               "(webseries_id, issue, issue_location) "
                               "VALUES ('"+ webseriesData[0] + "', '" + str(indexOfComic) + "', '" +
                               str(os.getcwd()) + saveTo[1:] + "\\" + str(indexOfComic) + ".gif" + "');")
            else:
                restart = False
        except IndexError:
            print("\rNo comic found at: " + comic.currentUrl + "\n")
        except HTTPError:
            cursor.execute("INSERT INTO missed_comics "
                           "(webseries_id, missed_URL) "
                           "VALUES ('" + webseriesData[0] + "', '" + comic.currentUrl + "');")


        cursor.execute("UPDATE webseries "
                       "SET latest_URL = '" + comic.currentUrl + "', latest_index = " + str(indexOfComic) + " "
                       "WHERE webseries_name = '" + comic.name + "';")

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