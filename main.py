import requests
import time
import json
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


URL = "https://wunderflats.com"
MAX_PAGE = 100

options = Options()
options.headless = True
WebDriver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)


def extract_flat_infos(flatURL):
    if not flatURL:
        return

    WebDriver.get(flatURL)
    html = WebDriver.page_source
    soup = BeautifulSoup(html, "html.parser")
    ret = soup.find(id="main")

    availableList = []
    if ret:
        partly_available = ret.find_all(
            "li", class_="MonthlyAvailabilityViewer-month--partlyAvailable")
        available = ret.find_all(
            "li", class_="MonthlyAvailabilityViewer-month--available")

        for p in partly_available:
            availableList.append(p.getText())

        for a in available:
            availableList.append(a.getText())

        return availableList


if __name__ == "__main__":
    page = 1
    last_page = 1

    flatsAvailable = []
    while page <= last_page and page <= MAX_PAGE:
        filters = "?minPrice=0&maxPrice=1600"
        url = "https://wunderflats.com/en/furnished-apartments/berlin/" + str(page) + filters
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

                availabilities = extract_flat_infos(flatURL)
                a = {"url": flatURL, "calendar": availabilities}
                flatsAvailable.append(a)

                print(a)
        last_page -= 1
        page += 1
        time.sleep(5)

    with open("availabilities.json", "w") as file:
        file.write(json.dumps(flatsAvailable))
