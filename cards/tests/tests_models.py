import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from cards.models import TrackParameter, Product


class TrackParameterModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='Alex',
            email='alex@gmail.com',
            password='Zxcvbn12345@'
        )
        track = TrackParameter.objects.create(
            article=74094830,
            start_at=datetime.datetime(2022, 12, 21, 21, 59, tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 12, 23, 2, 59, tzinfo=datetime.timezone.utc),
        )
        track.user.add(user)

    def test_article_max_length(self):
        track = TrackParameter.objects.get(id=2)
        field_max_length = track._meta.get_field('article').max_length
        self.assertEquals(field_max_length, 10)

    def test_article_label(self):
        track = TrackParameter.objects.get(id=2)
        field_label = track._meta.get_field('article').verbose_name
        self.assertEquals(field_label, 'артикул')

    def test_time_interval_default(self):
        track = TrackParameter.objects.get(id=2)
        field_default = track._meta.get_field('time_interval').default
        self.assertEquals(field_default, '1 hour')

    def test_time_interval_max_length(self):
        track = TrackParameter.objects.get(id=2)
        field_max_length = track._meta.get_field('time_interval').max_length
        self.assertEquals(field_max_length, 10)

    def test_time_interval_label(self):
        track = TrackParameter.objects.get(id=2)
        field_label = track._meta.get_field('time_interval').verbose_name
        self.assertEquals(field_label, 'Интервал отслеживания')

    def test_relation_to_user(self):
        track = TrackParameter.objects.get(id=2)
        username = track.user.all()[0].username
        self.assertEquals(username, 'Alex')

    def test_start_at_label(self):
        track = TrackParameter.objects.get(id=2)
        field_label = track._meta.get_field('start_at').verbose_name
        self.assertEquals(field_label, 'начало отслеживания')

    def test_end_at_label(self):
        track = TrackParameter.objects.get(id=2)
        field_label = track._meta.get_field('end_at').verbose_name
        self.assertEquals(field_label, 'Конец отслеживания')

    def test_user_label(self):
        track = TrackParameter.objects.get(id=2)
        field_label = track._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Пользователь')

    def test_object_name_in_admin(self):
        track = TrackParameter.objects.get(id=2)
        expected_object_name = f'{track.article}:{track.start_at}:{track.end_at}'
        self.assertEquals(expected_object_name, '74094830:2022-12-21 21:59:00+00:00:2022-12-23 02:59:00+00:00')


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='Alex',
            email='alex@gmail.com',
            password='Zxcvbn12345@'
        )
        track = TrackParameter.objects.create(
            article=74094830,
            start_at=datetime.datetime(2022, 4, 21, 21, 59, tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 4, 23, 2, 59, tzinfo=datetime.timezone.utc),
        )
        track.user.add(user)
        product = Product.objects.create(
            article=74094830,
            brand='adidas',
            name='Кроссовки',
            price_without_discount=999900,
            price_with_discount=739400,
            seller='ВАЙЛДБЕРРИЗ',
            time=datetime.datetime(2022, 4, 23, 2, 59, tzinfo=datetime.timezone.utc)
        )
        product.track.add(track)

    def test_article_max_length(self):
        product = Product.objects.get(id=1)
        field_max_length = product._meta.get_field('article').max_length
        self.assertEquals(field_max_length, 10)

    def test_article_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('article').verbose_name
        self.assertEquals(field_label, 'артикул')

    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        field_max_length = product._meta.get_field('name').max_length
        self.assertEquals(field_max_length, 100)

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'наименование товара')

    def test_price_without_discount_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price_without_discount').verbose_name
        self.assertEquals(field_label, 'Цена без скидки')

    def test_price_with_discount_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price_with_discount').verbose_name
        self.assertEquals(field_label, 'Цена со скидкой')

    def test_brand_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('brand').verbose_name
        self.assertEquals(field_label, 'бренд товара')

    def test_seller_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('seller').verbose_name
        self.assertEquals(field_label, 'поставщик')

    def test_track_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('track').verbose_name
        self.assertEquals(field_label, 'Параметры отслеживания')

    def test_relation_to_track(self):
        product = Product.objects.get(id=1)
        article = product.track.all()[0].article
        self.assertEquals(article, '74094830')

    def test_time_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('time').verbose_name
        self.assertEquals(field_label, 'Время отслеживания')

    def test_object_name_in_admin(self):
        product = Product.objects.get(id=1)
        expected_object_name = f'{product.brand}/ {product.name}/ {product.time.strftime("%Y-%m-%d %H:%M")}'
        self.assertEquals(expected_object_name, 'adidas/ Кроссовки/ 2022-04-23 02:59')

