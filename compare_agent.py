import requests
from bs4 import BeautifulSoup
import streamlit as st

SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
KEEPA_API_KEY = st.secrets["KEEPA_API_KEY"]

def search_google_shopping(query):
    url = f"https://serpapi.com/search.json?q={query}&engine=google_shopping&api_key={SERPAPI_KEY}"
    r = requests.get(url)
    results = r.json()
    products = results.get("shopping_results", [])
    if products:
        product = products[0]
        return {'source': 'Google', 'title': product['title'], 'price': product['price'], 'link': product['link']}
    return None

def search_ebay(query):
    url = f"https://www.ebay.co.uk/sch/i.html?_nkw={query.replace(' ', '+')}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    item = soup.select_one(".s-item__link")
    price = soup.select_one(".s-item__price")
    if item and price:
        return {'source': 'eBay', 'title': item.text.strip(), 'price': price.text.strip(), 'link': item['href']}
    return None

def search_amazon_keepa(asin):
    url = f"https://api.keepa.com/product?key={KEEPA_API_KEY}&domain=3&asin={asin}"
    r = requests.get(url).json()
    if r.get("products"):
        product = r["products"][0]
        title = product["title"]
        buy_box_price = product.get("buyBoxPriceHistory", [None])[-1]
        if buy_box_price:
            price = round(buy_box_price / 100, 2)
            return {'source': 'Amazon', 'title': title, 'price': f"£{price}", 'link': f"https://www.amazon.co.uk/dp/{asin}"}
    return None

def compare_prices(query, asin=None):
    results = []
    google = search_google_shopping(query)
    ebay = search_ebay(query)
    if asin:
        amazon = search_amazon_keepa(asin)
        if amazon:
            results.append(amazon)
    if google:
        results.append(google)
    if ebay:
        results.append(ebay)

    results.sort(key=lambda x: float(str(x['price']).replace("£", "").replace(",", "").split()[0]))
    return results
