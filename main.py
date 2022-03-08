import requests
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


URL = "https://wunderflats.com"

options = Options()
options.headless = True
WebDriver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)


def extract_flat_infos(flat):
    if not flat:
        return

    flatURL = URL + flat
    print("----------------------------")
    print(flatURL)
    WebDriver.get(flatURL)
    html = WebDriver.page_source
    soup = BeautifulSoup(html, "html.parser")
    ret = soup.find(id="main")
    if ret:
        calendar = ret.find_all("section", class_="ListingDetails-calendar")
        time.sleep(5)
        print(calendar)


if __name__ == "__main__":
    url = "https://wunderflats.com/en/furnished-apartments/berlin?minPrice=0&maxPrice=1453"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    ret = soup.find(id="main")
    flats = []
    if ret:
        items = ret.find_all("div", class_="ListingsList-item")
        for item in items:
            link = item.find("a")
            if link:
                flats.append(link["href"])
    for flat in flats:
        extract_flat_infos(flat)
