import datetime

from cards.models import TrackParameter, Product
from cards.parse_wildberries import get_wb_page_data
from django.utils.timezone import utc


def create_product(time_interval):
    for track in TrackParameter.objects.all():
        if track.start_at <= datetime.datetime.utcnow().replace(tzinfo=utc) <= track.end_at and track.time_interval == time_interval:
            article, brand, name, price_without_discount_penny, price_with_discount_penny, seller = get_wb_page_data(track.article)
            Product.objects.create(
                article=article,
                brand=brand,
                name=name,
                price_without_discount=price_without_discount_penny,
                price_with_discount=price_with_discount_penny,
                seller=seller,
                track=track,
            )