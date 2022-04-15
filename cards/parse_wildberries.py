import re
import requests

from bs4 import BeautifulSoup
from contextlib import contextmanager
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


BRAND_AND_NAME_CLASS = 'same-part-kt__header'
PRICE_WITHOUT_DISCOUNT_SELECTOR = '#infoBlockProductCard > div.same-part-kt__price-block > div > div > p > span'
PRICE_WITH_DISCOUNT_SELECTOR = '#infoBlockProductCard > div.same-part-kt__price-block > div > div > p > del'
SELLER_SELECTOR = '#infoBlockProductCard > div.same-part-kt__delivery-advantages > div.same-part-kt__seller-wrap > div > div.seller-details__info-wrap > div.seller-details__info > div.seller-details__title-wrap > a'


@contextmanager
def start_chrome_driver():
    """Launch the Chrome driver.

    At the end of the work, it close up all open windows,
    exits the browser and services, and release up all resources.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    try:
        yield driver
    finally:
        driver.quit()


def get_wb_page_data(article):
    url = f'https://www.wildberries.ru/catalog/{article}/detail.aspx'
    
    with start_chrome_driver() as driver:
        driver.get(url)
        
        brand_and_name = driver.find_element(By.CLASS_NAME, 'same-part-kt__header')

        soup = BeautifulSoup(brand_and_name.get_attribute('innerHTML'), 'lxml')
        
        brand, name = soup.text.split('/')
        brand_formatted = brand.strip()
        name_formatted = name.strip()

        price_without_discount = driver.find_element(By.CSS_SELECTOR, PRICE_WITHOUT_DISCOUNT_SELECTOR).text
        price_without_discount_penny = int(price_without_discount.split(' ')[0])*100
        
        price_with_discount = driver.find_element(By.CSS_SELECTOR, PRICE_WITH_DISCOUNT_SELECTOR).text
        price_with_discount_penny = int(re.sub(r'\s', '', price_with_discount).replace('₽', '')) * 100
   
        seller = WebDriverWait(driver, timeout=50).until(
            lambda x: x.find_element(By.CSS_SELECTOR, SELLER_SELECTOR)).text

    return int(article), brand_formatted, name_formatted, price_without_discount_penny, price_with_discount_penny, seller
