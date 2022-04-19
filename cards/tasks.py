from wildberries_cards_collection.celery import app
from .parse_wildberries import get_wb_page_data
from .create_product import create_product


@app.task
def update_product_data(article):
    get_wb_page_data(article)


@app.task
def update_beat_product_data_every_1_hour():
    create_product('1 hour')


@app.task
def update_beat_product_data_every_12_hours():
    create_product('12 hours')


@app.task
def update_beat_product_data_every_24_hours():
    create_product('24 hours')

