import re

from contextlib import contextmanager
from django.conf import settings
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, \
    StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


BRAND_SELECTOR = '#infoBlockProductCard > div.same-part-kt__header-wrap.hide-desktop > h1 > span:nth-child(1)'
NAME_SELECTOR = '#infoBlockProductCard > div.same-part-kt__header-wrap.hide-desktop > h1 > span:nth-child(2)'
PRICE_WITH_DISCOUNT_SELECTOR = '#infoBlockProductCard > div.same-part-kt__price-block > div > div > p > span'
PRICE_WITHOUT_DISCOUNT_SELECTOR = '#infoBlockProductCard > div.same-part-kt__price-block > div > div > p > del'
SELLER_BUTTON_SELECTOR = '#infoBlockProductCard > div.same-part-kt__delivery-advantages > div.same-part-kt__seller-wrap > div > div > div.seller__wrap > span.tip-info.seller__tip-info'
OTHER_SELLER_SELECTOR = '#infoBlockProductCard > div.same-part-kt__delivery-advantages > div.same-part-kt__seller-wrap > div > div.seller-details__info-wrap > div.seller-details__info > div.seller-details__title-wrap > a'
WB_SELLER_SELECTOR = '#infoBlockProductCard > div.same-part-kt__delivery-advantages > div.same-part-kt__seller-wrap > div > div > div.seller__wrap > span.seller__name.seller__name--short'


@contextmanager
def start_chrome_driver(selenium_server_url=settings.SELENIUM_SERVER_URL):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Remote(selenium_server_url, options=chrome_options)
    try:
        yield driver
    finally:
        driver.quit()


def get_wb_page_data(article):
    url = f'https://www.wildberries.ru/catalog/{article}/detail.aspx'

    with start_chrome_driver() as driver:

        driver.get(url)
        ignored_exceptions = (
            NoSuchElementException,
            StaleElementReferenceException,
        )
        wait_driver = WebDriverWait(driver,
                                    timeout=5,
                                    ignored_exceptions=ignored_exceptions)

        brand = wait_driver\
            .until(expected_conditions.
                   presence_of_element_located((By.CSS_SELECTOR, BRAND_SELECTOR)))\
            .text

        name = wait_driver\
            .until(expected_conditions.
                   presence_of_element_located((By.CSS_SELECTOR, NAME_SELECTOR)))\
            .text

        price_with_discount = wait_driver \
            .until(expected_conditions.
            presence_of_element_located(
            (By.CSS_SELECTOR, PRICE_WITH_DISCOUNT_SELECTOR))) \
            .text
        price_with_discount_penny = int(re.sub(r'\s', '', price_with_discount).replace('₽', '')) * 100

        try:
            price_without_discount = wait_driver \
                .until(expected_conditions.
                presence_of_element_located(
                (By.CSS_SELECTOR, PRICE_WITHOUT_DISCOUNT_SELECTOR))) \
                .text
            price_without_discount_penny = int(
                re.sub(r'\s', '', price_without_discount).replace('₽', '')) * 100
        except TimeoutException:
            price_without_discount_penny = price_with_discount_penny

        try:
            seller = wait_driver\
                .until(expected_conditions.
                       presence_of_element_located((By.CSS_SELECTOR, OTHER_SELLER_SELECTOR)))\
                .text
        except TimeoutException:
            seller = wait_driver \
                .until(expected_conditions.
                       presence_of_element_located((By.CSS_SELECTOR, WB_SELLER_SELECTOR))) \
                .text

    return int(article), brand, name, price_without_discount_penny, price_with_discount_penny, seller

