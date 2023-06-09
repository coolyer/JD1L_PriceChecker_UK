from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
# set up the Chrome driver and options
options = Options()
options.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# define the product so you rememeber
product = "Jack Daniels 1L"
sites = {
    "Tesco": "https://www.tesco.com/groceries/en-GB/products/264788740",
    "Asda": "https://groceries.asda.com/product/american-whiskey/jack-daniels-tennessee-whiskey/6037087",
    "Sainsbury's": "https://www.sainsburys.co.uk/gol-ui/product/jack-daniels-1l",
    "Morrisons": "https://groceries.morrisons.com/products/jack-daniel-s-tennessee-whiskey-217558011"
    
}



# search each site for the product and extract the price
print("Jack daniels price searcher")
tescoprice = None
asdaprice = None
sainsprice = None
morrisonprice = None
for site, url in sites.items():
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    try:
        if site == "Tesco":
            # wait for the price element to become visible
            price_elem = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".value")))
            # extract the price value from the element's text content
            price = "£" + price_elem.text.strip()
            tescoprice = "£" + price_elem.text.strip()
            
        elif site == "Sainsbury's":
            price_elem = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".pd__cost__retail-price")))
            # extract the price value from the element's text content
            price = price_elem.text.strip()
            sainsprice = price_elem.text.strip()
            
        elif site == "Asda":
            # wait for the price element to become visible
            price_elem = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".pdp-main-details__price")))
            # extract the price value from the element's text content
            price_text = price_elem.text.strip()
            # remove the "now" label from the price text using regular expressions
            price = re.sub(r'\bnow\b', '', price_text).strip()
            asdaprice = re.sub(r'\bnow\b', '', price_text).strip()
            
        elif site == "Morrisons":
            price_elem = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bop-price__current")))
            price = price_elem.text.strip()
            morrisonprice = price_elem.text.strip()
            
        else:
            price_elem = None
        if price_elem:
            price = price_elem.text
            print(site + ": " + price)
        else:
            price = "Price not found"
            print(site + ": " + price)
    except:
        print(site + ": Error scraping price")

# print the cheapest price found
if tescoprice is not None and asdaprice is not None and sainsprice is not None and morrisonprice is not None:
    # convert prices to float if they are in the correct format
    prices = {}
    for site, price in [("Tesco", tescoprice), ("Asda", asdaprice), ("Sainsbury's", sainsprice), ("Morrisons", morrisonprice)]:
        if isinstance(price, str) and price.startswith("£"):
            try:
                prices[site] = float(price[1:])
            except ValueError:
                print(f"Error converting price for {site}")
        else:
            prices[site] = None
    # find the cheapest price
    valid_prices = {site: price for site, price in prices.items() if price is not None}
    if len(valid_prices) > 0:
        cheapest_price = min(valid_prices.values())
        cheapest_sites = [site for site, price in valid_prices.items() if price == cheapest_price]
        if len(cheapest_sites) == 1:
            cheapest_site = cheapest_sites[0]
            cheapest_price_str = "£{:.2f}".format(cheapest_price)
            print(f"The cheapest price for {product} is found at {cheapest_site} for {cheapest_price_str}")
        else:
            cheapest_sites_str = ", ".join(cheapest_sites)
            cheapest_price_str = "£{:.2f}".format(cheapest_price)
            print(f"The cheapest price for {product} is found at {len(cheapest_sites)} sites: {cheapest_sites_str} for {cheapest_price_str}")
    else:
        print("Error: Could not find valid prices on one or more sites.")
else:
    print("Error: Could not find prices on one or more sites.")
driver.quit()
