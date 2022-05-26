from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup
from selenium import webdriver

class Product():
    def __init__(self, id, name, image_url="https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png"):
        self.id = id
        self.name = name
        self.image_url = image_url

def fetch_amazon_html(query, mwindow):
    ubar = mwindow.update_bar

    # Uses selenium to scrape off the needed information by launching a browser
    # instance and then automatically fetches the required information.
    QApplication.processEvents() # Used to prevent application from not responding while searching is going on
    driver = webdriver.Chrome()
    ubar(10)

    # Amazon uses the following syntax for the queries: 
    # If you search for heavy chainsaw, it becomes 'heavy+chainsaw' in the URL
    query.replace(' ','+')
    url = f"https://www.amazon.in/s?k={query}"
    ubar(20)

    driver.get(url)
    ubar(35)

    # Using beautiful soup to fetch the required info from the generated HTML
    return BeautifulSoup(driver.page_source, 'lxml')
    

def scrape_html(soup, mwindow):
    ubar = mwindow.update_bar

    # We will now find all the <div> elements that have the s-search-result property.
    product_soups = soup.find_all(
        'div', {'data-component-type': 's-search-result'})
    
    # Fetch the product IDs
    product_ids = [_.attrs['data-asin'] for _ in product_soups]
    
    ubar(5)
    product_objects = []

    _x = 0
    for product in product_soups:

        # Fetch the product title from HTML
        name = product.select_one(
            "span[class*='a-size-medium']").text

        # Get the image URL from HTML
        image_url = product.select_one("img[class*='s-image']").attrs['src']

        product = Product(id=product_ids[_x], name=name, image_url=image_url)
        product_objects.append(product)
        _x +=1
        ubar(5)

    return product_objects
