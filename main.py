import requests
import yaml
from yaml.loader import SafeLoader
import time
import json
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


CONFIG_FILE = "./config.yaml"
URL = "https://wunderflats.com"
MAX_PAGE = 100

options = Options()
options.headless = True
WebDriver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)


def getTextFromHtml(elem):
    if elem:
        return elem.getText()
    return ""


def getConfig():
    with open(CONFIG_FILE, "r") as file:
        data = yaml.load(file, Loader=SafeLoader)
    return data


def extract_flat_infos(flatURL):
    if not flatURL:
        return

    WebDriver.get(flatURL)
    html = WebDriver.page_source
    soup = BeautifulSoup(html, "html.parser")
    ret = soup.find(id="main")

    availableList = []
    if ret:
        rooms = ret.find(
            "span", { "class": "ListingDetails-statsElt rooms" })
        beds = ret.find(
            "span", { "class": "ListingDetails-statsElt beds"})
        minStay = ret.find(
            "span", { "class": "ListingDetails-statsElt minBookingDuration" })
        price = ret.find(
            "strong", { "class": "ListingPriceText-value" })

        partly_available = ret.find_all(
            "li", class_="MonthlyAvailabilityViewer-month--partlyAvailable")
        available = ret.find_all(
            "li", class_="MonthlyAvailabilityViewer-month--available")

        for p in partly_available:
            availableList.append(p.getText())

        for a in available:
            availableList.append(a.getText())

        return {
            "availabilities": availableList,
            "price": getTextFromHtml(price),
            "rooms": getTextFromHtml(rooms),
            "beds": getTextFromHtml(beds),
            "minStay": getTextFromHtml(minStay)
        }


if __name__ == "__main__":
    conf = getConfig()
    page = 1
    last_page = 1

    allFlats = []
    while page <= last_page and page <= MAX_PAGE:
        filters = "?minPrice={}&maxPrice={}".format(conf["minPrice"], conf["maxPrice"])
        url = "https://wunderflats.com/en/furnished-apartments/{city}/{page}/{filters}".format(city=conf["city"], page=page, filters=filters)

        print("url = ", url)
        site = requests.get(url)
        soup = BeautifulSoup(site.content, "html.parser")
        ret = soup.find(id="main")
        flats = []
        if ret:
            items = ret.find_all("div", class_="ListingsList-item")
            if last_page == 1:
                pages = ret.find_all("a", class_="Pagination-item")
                last_page = pages[2].getText()
                last_page = int(last_page)
                print("last_page = ", last_page)

            for item in items:
                link = item.find("a")
                if link:
                    flats.append(link["href"])

            for flat in flats:
                flatURL = URL + flat

                infos = extract_flat_infos(flatURL)
                a = {"url": flatURL,
                     "calendar": infos["availabilities"],
                     "price": infos["price"],
                     "rooms": infos["rooms"],
                     "beds": infos["beds"],
                     "minStay": infos["minStay"],
                     }
                allFlats.append(a)

                print(a)
        last_page -= 1
        page += 1
        time.sleep(5)

    # store all flats
    with open("all_flats.json", "w") as file:
        file.write(json.dumps(allFlats))

    # check for availability
    flatMatchingAvailabitlies = []
    for f in allFlats:
        if conf["availableFrom"] in f["calendar"]:
            flatMatchingAvailabitlies.append(f)

    with open("flats_available.json", "w") as file:
        file.write(json.dumps(flatMatchingAvailabitlies))

    print("flatMatchingAvailabitlies: \n", flatMatchingAvailabitlies)
