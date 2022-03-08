import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    URL = "https://wunderflats.com/en/furnished-apartments/berlin?minPrice=0&maxPrice=1453"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    ret = soup.find(id="main")
    if ret:
        items = ret.find_all("div", class_="ListingsList-item")
        for item in items:
            print(item.prettify())
