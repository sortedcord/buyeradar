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

def fetch_amazon_html(query, mwindow, debug, debugfile=None):
    # update_bar and update_console are variables that are used to update the progress bar and console
    update_bar = mwindow.update_bar
    update_console= mwindow.updateConsole

    if debugfile is not None and debug:
        try:
            with open(debugfile) as f:
                lines = f.read()
                # if the file is empty, update using suitable message and set debug to false
                if lines == '':
                    update_console('given debug file is empty')
                    update_console('Fetching HTML from online source')
                    debug = 'force'
                    
        except:
            update_console("Could not read file")
            update_console('Fetching HTML from online source')
            debug = 'force'
        else:
            if debug != 'force':
                return BeautifulSoup(lines, 'lxml')
                

    if not debug or debug == 'force':
        # Uses selenium to scrape off the needed information by launching a browser
        # instance and then automatically fetches the required information.
        mwindow.updateConsole("Setting Chrome Options")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        QApplication.processEvents() # Used to prevent application from not responding while searching is going on
        driver = webdriver.Chrome(chrome_options=chrome_options)
        update_bar(10)

        # Amazon uses the following syntax for the queries: 
        # If you search for heavy chainsaw, it becomes 'heavy+chainsaw' in the URL
        query.replace(' ','+')
        url = f"https://www.amazon.in/s?k={query}"
        update_bar(20)

        update_console("Fetching Page URL")
        try:
            driver.get(url)
        except:
            update_console("Could not fetch data")
            return
        else:
            update_console("Fetched HTML successfully")
        update_bar(35)

        if debug == 'force':
        # Using beautiful soup to fetch the required info from the generated HTML
            with open("test.txt", "w+") as f:
                f.write(driver.page_source)
                # Update console with suitable message
                update_console("Saved HTML to test.txt")
        return BeautifulSoup(driver.page_source, 'lxml')
    

def scrape_html(soup, mwindow):
    update_bar = mwindow.update_bar
    update_console= mwindow.updateConsole

    # We will now find all the <div> elements that have the s-search-result property.
    product_soups = soup.find_all(
        'div', {'data-component-type': 's-search-result'})
    
    # Fetch the product IDs
    product_ids = [_.attrs['data-asin'] for _ in product_soups]
    update_console("Fetched Product IDs")
    
    update_bar(5)
    product_objects = []

    _x = 0
    for product in product_soups:
        if _x > 15:
            break
        # Get the displayed price of the product from HTML

        update_console(f"[Product {_x+1}] Fetching Price")
        try:
            price = product.select_one("span[class*='price-whole']").text
        except AttributeError:
            price = 'NAN'
        else:
            update_console(f"[Product {_x+1}] Fetched Price Successfully")
        

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
                update_console(f"[Product {_x+1}] Fetched name successfully")
        else:
            update_console(f"[Product {_x+1}] Fetched name successfully")


        # Get the image URL from HTML
        try:
            image_url = product.select_one("img[class*='s-image']").attrs['src']
        except:
            update_console(f"[Product {_x+1}] Could not fetch image URL")
        else:
            update_console(f"[Product {_x+1}] Fetched image URL")

        update_console(f"[Product {_x+1}] Creating Product Object")
        product = Product(id=product_ids[_x], price=price, name=name, image_url=image_url)
        update_console(f"[Product {_x+1}] Created Product Object")
        product_objects.append(product)
        update_console(f"[Product {_x+1}] Added to search result list")
        _x +=1
        update_bar(5)

    update_console("Parsed Product Objects from fetched HTML")
    return product_objects


def trim_name(string):
    return (string[:50] + '..') if len(string) > 50 else string 