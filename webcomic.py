import requests
import lxml.html
from urllib.request import *
from urllib.parse import *
from urllib.error import *

class Webcomic(object):
    headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }

    def __init__(self, name, base, currentUrl, nextUrl, comicUrl):
        self.name = name
        self.baseUrl = base
        self.currentUrl = currentUrl
        self.nextUrl = nextUrl
        self.comicLocation = comicUrl

    def getComic(self, saveLocation, number):
        website = requests.get(self.currentUrl, headers=self.headers)
        document = lxml.html.fromstring(website.content)
        imageLocation = document.xpath(self.comicLocation)
        if len(imageLocation) < 1:
            raise IndexError
        if len(imageLocation) > 1:
            for i,image in enumerate(imageLocation):
                cleanedImageLocation = image.replace(" ", "%20")
                try:
                    urlretrieve(urljoin("http:", cleanedImageLocation),
                                saveLocation + str(number).zfill(5) + "-" + str(i).zfill(2) + ".gif")
                except HTTPError as err:
                    print(err.read().decode("utf8"))
        else:
            try:
                cleanedImageLocation = imageLocation[0].replace(" ", "%20")
                urlretrieve(urljoin("http:", cleanedImageLocation), saveLocation + str(number).zfill(5) + ".gif")
            except HTTPError as err:
                print(err.read().decode("utf8"))
                raise HTTPError

    def getNext(self):
        website = requests.get(self.currentUrl, headers=self.headers)
        document = lxml.html.fromstring(website.content)
        nextPageUrl = document.xpath(self.nextUrl)
        finalUrl = urljoin(self.baseUrl, nextPageUrl[0])
        return finalUrl