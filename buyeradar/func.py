import datetime
import random
from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sqlite3


class Product():
    """
    All classes have a function called __init__(), which is always executed when the class is being initiated.
    Use the __init__() function to assign values to object properties when the object is being created
    """

    def __init__(self, id, price, name, image_url, source="Amazon"):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.price = price
        self.source = source

    # This method is invoked when the object is printed
    def __str__(self) -> str:
        return f"Product: {self.name} from {self.source} with price {self.price}"


"""
This function will be called when the user clicks the search button
It will scrape the HTML from the Amazon website and return a list of Product objects
The Product objects will be used to populate the table later on
"""


def fetch_amazon_html(query, mwindow, debug, debugfile=None):
    # update_bar and update_console are variables that are used to update the progress
    # bar and console
    update_bar = mwindow.update_bar
    update_console = mwindow.updateConsole

    # if a debugfile is passed and debug mode is
    # set to true, then it will read the debugfile
    if debugfile is not None and debug:
        try:
            with open(debugfile) as f:
                lines = f.read()
                # if the file is empty, update using suitable message and set debug to false
                if lines == '':
                    update_console('given debug file is empty')
                    update_console('Fetching HTML from online source')
                    debug = 'force'
                    # force means that the debug mode has switched to fallback mode.

        except:
            update_console("Could not read file")
            update_console('Fetching HTML from online source')
            debug = 'force'
        else:
            if debug != 'force':
                return BeautifulSoup(lines, 'lxml')

    # Check if the user has entered the product url instad
    if query.startswith("https://www.amazon.in/"):
        url = query
        return fetch_amazon_page_content(url, mwindow)

    if not debug or debug == 'force':
        # Uses selenium to scrape off the needed information by launching a browser
        # instance and then automatically fetches the required information.
        mwindow.updateConsole("Setting Chrome Options")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"])
        QApplication.processEvents()  # Used to prevent application from not responding
        driver = webdriver.Chrome(chrome_options=chrome_options)
        update_bar(10)

        # Amazon uses the following syntax for the queries:
        # If you search for heavy chainsaw, it becomes 'heavy+chainsaw' in the URL
        query.replace(' ', '+')
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

        # if the page source contains the string "No results for " then return None
        if "No results for " in str(driver.page_source):
            update_console("No results found")
            return None
        return BeautifulSoup(driver.page_source, 'lxml')


"""
This function will be invoked if the user has entered the product url
instead of the product name
"""


def fetch_amazon_page_content(url, mwindow=None):
    # The user has entered the product url, so the function will fetch
    # information from the product page and not the search page.

    if mwindow is not None:
        update_bar = mwindow.update_bar
        update_console = mwindow.updateConsole
    else:
        # This would happen if the function is not called from the main window
        # Create a dummy class instead
        class mwindow():
            def update_bar(value):
                pass

            def updateConsole(value):
                pass
        
        update_bar = mwindow.update_bar
        update_console = mwindow.updateConsole

    mwindow.updateConsole("Setting Chrome Options")
    chrome_options = Options()
    # Headless options hides the browser window from showing up
    chrome_options.add_argument("--headless")
    # These options are used to prevent the browser from
    # logging unnecessary information
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])

    QApplication.processEvents()  # Used to prevent application from not responding
    driver = webdriver.Chrome(chrome_options=chrome_options)
    update_bar(10)

    # We will try to get the ASIN number from the URL that the user has
    # provided and then reformat it again to fetch the product page
    try:
        asin = url.split("/dp/")[1].split("/")[0]
    except:  # If the url is invalid, return None
        update_console("Invalid URL")
        return []
    url = f"https://www.amazon.in/dp/{asin}"
    update_console("Shortened URL to {}".format(url))
    update_bar(20)

    QApplication.processEvents()
    update_console("Fetching Page URL")
    QApplication.processEvents()
    try:
        driver.get(url)
    except:
        update_console("Could not fetch data")
        return
    else:
        update_console("Fetched HTML successfully")

    soup = BeautifulSoup(driver.page_source, 'lxml')

    QApplication.processEvents()

    ##########
    # Filtering Data
    ##########

    product_name = trim_name(soup.find(id="productTitle").text.strip())
    # find a span with id as 'price'
    try:
        price = soup.find(id="price").text.strip()[1:].replace(',', '')
    except:
        # If the price is not found using the above route
        try:
            price = soup.find(class_="a-price-whole").text.replace(',', '')
        except:
            price = 0
    product_id = asin

    # get the src attribute of the image tag with class containing "a-dynamic-image"
    image_url = soup.find("img", class_="a-dynamic-image")['src']
    update_bar(35)

    # Create a product object and return it
    product = Product(product_id, price, product_name, image_url)
    return product


def scrape_html(soup, mwindow):
    update_bar = mwindow.update_bar
    update_console = mwindow.updateConsole

    # We will now find all the <div> that have the s-search-result property.
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
            # Try to find the HTML tag that has the class containing "a-price-whole"
            price = product.select_one("span[class*='price-whole']").text
            # Remove the commas from the price
            price = price.replace(',', '').split(".")[0]
            price = int(price)
        except AttributeError:
            # If the price is not found using the above route
            price = "0"
        else:
            update_console(f"[Product {_x+1}] Fetched Price Successfully")

        # Fetch the product title from HTML
        try:
            # Try to find the HTML tag that has the class containing "a-size-medium"
            name = product.select_one(
                "span[class*='a-size-medium']").text
        except AttributeError:
            # If the product name is not found using the above route
            # then try to find the HTML tag that has the class containing "a-size-base-plus"
            try:
                name = product.select_one(
                    "span[class*='a-size-base-plus']").text
            except AttributeError:
                # If the product name is still not found:
                name = 'NAN'

            else:
                update_console(f"[Product {_x+1}] Fetched name successfully")
        else:
            update_console(f"[Product {_x+1}] Fetched name successfully")

        # Get the image URL from HTML
        try:
            # Try to find the HTML tag that has the class containing "s-image"
            image_url = product.select_one(
                "img[class*='s-image']").attrs['src']
        except:
            update_console(f"[Product {_x+1}] Could not fetch image URL")
        else:
            update_console(f"[Product {_x+1}] Fetched image URL")

        update_console(f"[Product {_x+1}] Creating Product Object")
        product = Product(
            id=product_ids[_x], price=price, name=name, image_url=image_url)
        update_console(f"[Product {_x+1}] Created Product Object")
        product_objects.append(product)
        update_console(f"[Product {_x+1}] Added to search result list")
        _x += 1
        update_bar(5)

    update_console("Parsed Product Objects from fetched HTML")
    return product_objects


def trim_name(string):
    return (string[:50] + '..') if len(string) > 50 else string


def save_to_database(product):
    print("Tack button clicked")

    pid = product.id
    pname = product.name
    image_url = product.image_url
    pprice = float(int(str(product.price).split('.')[0]))
    while True:
        flag = True
        recordid = random.randint(100, 999)

        # Check whether recordid is already there or not
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()

        command = f"select recordid from product;"
        cursor.execute(command)

        data = cursor.fetchall()
        for i in data:
            if recordid == i[0]:
                flag = True
            else:
                flag = False
        if not flag:
            break


    # Get the current date time in the format of 2020-05-09 04:01:02
    recordtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    psource = "amazon.in"

    # Code here to save to
    # database

    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()

    command = f"insert into product values('{recordid}','{pid}','{pname}','{pprice}','{psource}', '{image_url}', '{recordtime}');"

    cursor.execute(command)
    conn.commit()
    print("Saved in database")
    cursor.close()


def load_unique_from_database():

    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()

    command3 = "select * from product"
    cursor.execute(command3)

    tuple2 = cursor.fetchall()
    dictionary = {}
    for i in range(len(tuple2)):
        dictionary[tuple2[i][1]] = tuple2[i]
    info_of_unique_pid = list(dictionary.values())
    return info_of_unique_pid


def load_single_product(pid):
    # Takes in the product id as the argument and returns all the records
    # of that specific product in descing order based on time of the entry

    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    command = f"select * from product where pid='{pid}' order by recordtime DESC;"
    cursor.execute(command)
    data = cursor.fetchall()
    cursor.close()

    return data


def create_table(dummy=True):
    # Creates a table in the database if it does not exist

    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    command = """create table if not exists 
product(recordid varchar(50) primary key, 
pid varchar(50) NOT NULL, 
pname varchar(200) NOT NULL, 
pprice decimal(15,2), 
psource varchar(200),
image_url varchar(200), 
recordtime datetime default current_timestamp);"""

    cursor.execute(command)
    conn.commit()
    # If the user sets dummy to true, then the function will create
    # dummy/random records to add to the database table
    if dummy:
        for i in range(10):
            product_id = random.randint(1000000000, 9999999999)
            product_name = f"Dummy Product {random.randint(1,100)}"
            for j in range(random.randint(0, 10)):
                price = random.randint(1000, 9999)
                record_id = random.randint(100, 999)
                datetime = f"2020-0{random.randint(1,9)}-0{random.randint(1,9)} 0{random.randint(1,9)}:0{random.randint(1,9)}:0{random.randint(1,9)}"
                command = f"insert into product values('{record_id}','{product_id}','{product_name}','{price}','amazon.in','https://images-na.ssl-images-amazon.com/images/I/71ZyNqZQJlL._AC_SL1500_.jpg','{datetime}');"
                cursor.execute(command)
                conn.commit()
                j += 1
            # asd = random_datetime.strftime("%Y-%m-%d %H:%M:%S")
            i += 1
    cursor.close()


if __name__ == "__main__":
    print("This is a module, not a script. Please run main.py instead")

    load_unique_from_database()
