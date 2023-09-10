from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import random
import time

input_product_name = input("Aradağınız ürünü giriniz.")


class Scrapper:
    def __init__(self, url):
        self.url = url
        self.user_agent = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 "
            "Safari/537.36")

        # Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument(f"user-agent={self.user_agent}")
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')  # May be required in some cases
        self.driver = webdriver.Chrome(options=self.chrome_options)

        self.product_list = []
        self.price_list = []

    def scrape_trendyol(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located(
            (By.XPATH, '//*[@id="sfx-discovery-search-suggestions"]/div/div[1]/input')))
        search_bar = self.driver.find_element(By.XPATH, '//*[@id="sfx-discovery-search-suggestions"]/div/div[1]/input')
        time.sleep(random.randint(2, 5))
        search_bar.send_keys(input_product_name)
        time.sleep(random.randint(2, 5))
        search_bar.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 20).until(
            ec.visibility_of_element_located((By.XPATH, '//*[@id="search-app"]/div/div[1]/div[2]/div[1]/div[1]/div')))
        product_prices = self.driver.find_elements(By.CLASS_NAME, 'prc-box-dscntd')
        product_names = self.driver.find_elements(By.CLASS_NAME, 'prdct-desc-cntnr-name')

        self.product_list = []
        self.price_list = []

        for product in product_names:
            self.product_list.append(product.text)
        for price in product_prices:
            self.price_list.append(price.text)

        print("TRENDYOL SONUÇLARI: ")

        for product_name, product_price in zip(self.product_list, self.price_list):
            print(f"Ürün adı: {product_name} - Ürün Fiyatı: {product_price}")

    def scrape_hepsi_burada(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 20).until(
            ec.visibility_of_element_located((By.CLASS_NAME, 'searchResultSummaryBar-CbyZhv5896ASVcYBLKmx')))
        time.sleep(random.randint(2, 5))
        product_names = self.driver.find_elements(By.CLASS_NAME, 'moria-ProductCard-fHiOwt')
        product_prices = self.driver.find_elements(By.CLASS_NAME, 'moria-ProductCard-giQTR')

        self.product_list = []
        self.price_list = []

        for product in product_names:
            self.product_list.append(product.text)
        for price in product_prices:
            self.price_list.append(price.text)

        print("\nHEPSİBURADA SONUÇLARI: ")

        for product_name, product_price in zip(self.product_list, self.price_list):
            print(f"Ürün adı: {product_name} - Ürün Fiyatı: {product_price}")

    def scrape_amazon(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located(
            (By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/span/div/div/span')))
        product_names = self.driver.find_elements(By.CLASS_NAME, 'a-size-base-plus')
        product_prices = self.driver.find_elements(By.CLASS_NAME, 'a-price-whole')

        self.product_list = []
        self.price_list = []

        for product in product_names:
            self.product_list.append(product.text)
        for price in product_prices:
            self.price_list.append(price.text)

        print("\nAMAZON SONUÇLARI: ")

        for product_name, product_price in zip(self.product_list, self.price_list):
            print(f"Ürün adı: {product_name} - Ürün Fiyatı: {product_price}")


# URLS in list
urls = [
    "https://www.trendyol.com",
    f"https://www.hepsiburada.com/ara?q={input_product_name}",
    f"https://www.amazon.com.tr/s?k={input_product_name}",
]

# Scrape each URLS
for url in urls:
    scraper = Scrapper(url)
    if "trendyol.com" in url:
        scraper.scrape_trendyol()
    elif "hepsiburada.com" in url:
        scraper.scrape_hepsi_burada()
    elif "amazon.com.tr" in url:
        scraper.scrape_amazon()
