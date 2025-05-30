import requests
from bs4 import BeautifulSoup
import streamlit as st

SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
KEEPA_API_KEY = st.secrets["KEEPA_API_KEY"]

def debug_log(label, data):
    with st.expander(f"Debug: {label}"):
        st.write(data)

@st.cache_data(show_spinner=False)
def search_google_shopping(query):
    url = f"https://serpapi.com/search.json?q={query}&engine=google_shopping&api_key={SERPAPI_KEY}"
    r = requests.get(url)
    results = r.json()
    debug_log("Google Raw Response", results)
    products = results.get("shopping_results", [])
    if products:
        product = products[0]
        return {
            'source': 'Google',
            'title': product.get('title'),
            'price': product.get('price'),
            'link': product.get('link'),
            'image': product.get('thumbnail')
        }
    return None

@st.cache_data(show_spinner=False)
def search_ebay(query):
    url = f"https://www.ebay.co.uk/sch/i.html?_nkw={query.replace(' ', '+')}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    debug_log("eBay HTML Sample", soup.prettify()[:500])
    item = soup.select_one(".s-item__link")
    price = soup.select_one(".s-item__price")
    image = soup.select_one(".s-item__image-img")
    if item and price:
        return {
            'source': 'eBay',
            'title': item.text.strip(),
            'price': price.text.strip(),
            'link': item['href'],
            'image': image['src'] if image else None
        }
    return None

@st.cache_data(show_spinner=False)
def search_amazon_keepa(asin):
    url = f"https://api.keepa.com/product?key={KEEPA_API_KEY}&domain=3&asin={asin}"
    r = requests.get(url).json()
    debug_log("Keepa Raw Response", r)
    if r.get("products"):
        product = r["products"][0]
        title = product.get("title", "Unknown Title")
        image = product.get("imagesCSV", "").split(",")[0]
        buy_box_price = product.get("buyBoxPriceHistory", [None])[-1]
        if buy_box_price:
            price = round(buy_box_price / 100, 2)
            return {
                'source': 'Amazon',
                'title': title,
                'price': f"£{price}",
                'link': f"https://www.amazon.co.uk/dp/{asin}",
                'image': f"https://images-na.ssl-images-amazon.com/images/I/{image}" if image else None
            }
    return None

def compare_prices(query, asin=None):
    results = []
    google = search_google_shopping(query)
    ebay = search_ebay(query)
    amazon = search_amazon_keepa(asin) if asin else None

    for result in [amazon, google, ebay]:
        if result:
            results.append(result)

    def safe_price(r):
        try:
            return float(str(r['price']).replace("£", "").replace(",", "").split()[0])
        except:
            return float('inf')

    try:
        results.sort(key=safe_price)
    except Exception as e:
        st.error(f"Sorting failed: {e}")
    return results
