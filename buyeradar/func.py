from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Product():
    def __init__(self, id, price, name, image_url="https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png"):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.price = price

def fetch_amazon_html(query, mwindow, debugfile=None):
    ubar = mwindow.update_bar
    ucon= mwindow.updateConsole

    if debugfile is not None:
        try:
            with open(debugfile) as f:
                lines = f.read()
        except:
            ucon("Could not read file")
        return BeautifulSoup(lines, 'lxml')


    # Uses selenium to scrape off the needed information by launching a browser
    # instance and then automatically fetches the required information.
    mwindow.updateConsole("Setting Chrome Options")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    QApplication.processEvents() # Used to prevent application from not responding while searching is going on
    driver = webdriver.Chrome(chrome_options=chrome_options)
    ubar(10)

    # Amazon uses the following syntax for the queries: 
    # If you search for heavy chainsaw, it becomes 'heavy+chainsaw' in the URL
    query.replace(' ','+')
    url = f"https://www.amazon.in/s?k={query}"
    ubar(20)

    ucon("Fetching Page URL")
    try:
        driver.get(url)
    except:
        ucon("Could not fetch data")
        return
    else:
        ucon("Fetched HTML successfully")
    ubar(35)

    # Using beautiful soup to fetch the required info from the generated HTML
    # with open("test.txt", "w+") as f:
    #     f.write(driver.page_source)
    return BeautifulSoup(driver.page_source, 'lxml')
    

def scrape_html(soup, mwindow):
    ubar = mwindow.update_bar
    ucon= mwindow.updateConsole

    # We will now find all the <div> elements that have the s-search-result property.
    product_soups = soup.find_all(
        'div', {'data-component-type': 's-search-result'})
    
    # Fetch the product IDs
    product_ids = [_.attrs['data-asin'] for _ in product_soups]
    ucon("Fetched Product IDs")
    
    ubar(5)
    product_objects = []

    _x = 0
    for product in product_soups:
        if _x > 15:
            break
        # Get the displayed price of the product from HTML

        ucon(f"[Product {_x+1}] Fetching Price")
        try:
            price = product.select_one("span[class*='price-whole']").text
        except AttributeError:
            price = 'NAN'
        else:
            ucon(f"[Product {_x+1}] Fetched Price Successfully")
        

        # Fetch the product title from HTML
        try:
            name = product.select_one(
                "span[class*='a-size-medium']").text
        except AttributeError:
            try:
                name = product.select_one(
                    "span[class*='a-size-base-plus']").text
            except AttributeError:
                name = 'NAN'
            else:
                ucon(f"[Product {_x+1}] Fetched name successfully")
        else:
            ucon(f"[Product {_x+1}] Fetched name successfully")


        # Get the image URL from HTML
        try:
            image_url = product.select_one("img[class*='s-image']").attrs['src']
        except:
            ucon(f"[Product {_x+1}] Could not fetch image URL")
        else:
            ucon(f"[Product {_x+1}] Fetched image URL")

        ucon(f"[Product {_x+1}] Creating Product Object")
        product = Product(id=product_ids[_x], price=price, name=name, image_url=image_url)
        ucon(f"[Product {_x+1}] Created Product Object")
        product_objects.append(product)
        ucon(f"[Product {_x+1}] Added to search result list")
        _x +=1
        ubar(5)

    ucon("Parsed Product Objects from fetched HTML")
    return product_objects


def trim_name(string):
    return (string[:50] + '..') if len(string) > 50 else string