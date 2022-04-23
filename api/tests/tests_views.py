import datetime
from django.contrib.auth import get_user_model

from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from cards.models import TrackParameter, Product
from api.serializers import TrackParameterListSerializer
from rest_framework.test import APIClient


class EndpointsLoginRequiredTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required_create_new_track(self):

        res = self.client.get(reverse('create_new_track'))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_get_all_tracks(self):

        res = self.client.get(reverse('get_all_tracks'))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_get_track(self):

        res = self.client.get(reverse('get_track', args=[1]))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_get_track_products(self):

        res = self.client.get(reverse('get_track_products', args=[1]))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_get_user_products(self):

        res = self.client.get(reverse('get_user_products'))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_get_product_info(self):

        res = self.client.get(reverse('get_product_info', args=['12345678']))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateNewTrackParameterTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@mail.ru',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.valid_payload = {
            'article': '74094830',
            'start_at': datetime.datetime(2022, 12, 21, 21, 59,
                                          tzinfo=datetime.timezone.utc),
            'end_at': datetime.datetime(2022, 12, 23, 2, 59,
                                        tzinfo=datetime.timezone.utc),
        }

        self.invalid_article_payload = {
            'article': '',
            'start_at': datetime.datetime(2022, 12, 29, 21, 59,
                                          tzinfo=datetime.timezone.utc),
            'end_at': datetime.datetime(2022, 12, 30, 2, 59,
                                        tzinfo=datetime.timezone.utc),
        }

        self.invalid_start_at_payload = {
            'article': '74094830',
            'start_at': datetime.datetime(2023, 12, 21, 21, 59,
                                          tzinfo=datetime.timezone.utc),
            'end_at': datetime.datetime(2022, 12, 23, 2, 59,
                                        tzinfo=datetime.timezone.utc),
        }

        self.invalid_end_at_payload = {
            'article': '74094830',
            'start_at': datetime.datetime(2022, 12, 21, 21, 59,
                                          tzinfo=datetime.timezone.utc),
            'end_at': datetime.datetime(2022, 11, 23, 2, 59,
                                        tzinfo=datetime.timezone.utc),
        }

    def test_create_valid_track_parameter(self):

        response = self.client.post(
            reverse('create_new_track'),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_article(self):
        response = self.client.post(
            reverse('create_new_track'),
            data=self.invalid_article_payload,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_start_at(self):
        response = self.client.post(
            reverse('create_new_track'),
            data=self.invalid_start_at_payload,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_end_at(self):
        response = self.client.post(
            reverse('create_new_track'),
            data=self.invalid_end_at_payload,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TrackParameterListTest(TestCase):
    def setUp(self):
        self.user2 = get_user_model().objects.create_user(
            'test@mail.ru',
            'testpass'
        )
        self.user3 = get_user_model().objects.create_user(
            'test1@mail.ru',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user2)

    def test_list_only_current_user(self):
        track1 = TrackParameter.objects.create(
            article='74094830',
            start_at=datetime.datetime(2022, 12, 21, 21, 59,
                                      tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 12, 23, 2, 59,
                                    tzinfo=datetime.timezone.utc),
        )
        track1.user.add(self.user2)

        track2 = TrackParameter.objects.create(
            article=74094831,
            start_at=datetime.datetime(2022, 11, 21, 21, 59,
                                       tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 11, 23, 2, 59,
                                     tzinfo=datetime.timezone.utc),
        )
        track2.user.add(self.user3)

        response = self.client.get(reverse('get_all_tracks'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class TrackParameterDetailTest(TestCase):

    def setUp(self):
        self.user2 = get_user_model().objects.create_user(
            'test@mail.ru',
            'testpass'
        )
        self.user3 = get_user_model().objects.create_user(
            'test1@mail.ru',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user2)

    def test_track_parameter_detail_user(self):
        track1 = TrackParameter.objects.create(
            article=74094830,
            start_at=datetime.datetime(2022, 12, 21, 21, 59,
                                      tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 12, 23, 2, 59,
                                    tzinfo=datetime.timezone.utc),
        )
        track1.user.add(self.user2)

        track2 = TrackParameter.objects.create(
            article=74094831,
            start_at=datetime.datetime(2022, 11, 21, 21, 59,
                                       tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 11, 23, 2, 59,
                                     tzinfo=datetime.timezone.utc),
        )
        track2.user.add(self.user3)

        response = self.client.get(reverse('get_track', args=[9]))
        serializer = TrackParameterListSerializer(TrackParameter.objects.get(id=9))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class ProductsListForTrackParameterTest(TestCase):

    def setUp(self):
        self.user4 = get_user_model().objects.create_user(
            'test4@mail.ru',
            'testpass'
        )
        self.user5 = get_user_model().objects.create_user(
            'test5@mail.ru',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user4)

    def test_products_list_for_track_parameter(self):
        track1 = TrackParameter.objects.create(
            article='74094831',
            start_at=datetime.datetime(2022, 12, 21, 21, 59,
                                      tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 12, 23, 2, 59,
                                    tzinfo=datetime.timezone.utc),
        )
        track1.user.add(self.user4)

        track2 = TrackParameter.objects.create(
            article='74094831',
            start_at=datetime.datetime(2022, 11, 21, 21, 59,
                                       tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 11, 23, 2, 59,
                                     tzinfo=datetime.timezone.utc),
        )
        track2.user.add(self.user5)

        product1 = Product.objects.create(
            article='74094830',
            brand='adidas',
            name='Кроссовки',
            price_without_discount=999900,
            price_with_discount=739400,
            seller='ВАЙЛДБЕРРИЗ',
            time=datetime.datetime(2022, 4, 23, 2, 59,
                                   tzinfo=datetime.timezone.utc)
        )
        product1.track.add(track1)
        product2 = Product.objects.create(
            article='74094831',
            brand='puma',
            name='Кроссовки',
            price_without_discount=999900,
            price_with_discount=739400,
            seller='ВАЙЛДБЕРРИЗ',
            time=datetime.datetime(2022, 4, 23, 2, 59,
                                   tzinfo=datetime.timezone.utc)
        )
        product2.track.add(track2)
        product3 = Product.objects.create(
            article='74094833',
            brand='puma1',
            name='Кроссовки',
            price_without_discount=999900,
            price_with_discount=739400,
            seller='ВАЙЛДБЕРРИЗ',
            time=datetime.datetime(2022, 4, 23, 2, 59,
                                   tzinfo=datetime.timezone.utc)
        )
        product3.track.add(track1)

        response = self.client.get(reverse('get_track_products', args=[5]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['article'], product1.article)
        self.assertEqual(response.data['results'][1]['article'], product3.article)


class ProductsListViewTest(TestCase):

    def setUp(self):
        self.user6 = get_user_model().objects.create_user(
            'test4@mail.ru',
            'testpass'
        )
        self.user7 = get_user_model().objects.create_user(
            'test5@mail.ru',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user6)

    def test_products_list_for_all_tracks(self):
        track1 = TrackParameter.objects.create(
            article='74094834',
            start_at=datetime.datetime(2022, 12, 21, 21, 59,
                                      tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 12, 23, 2, 59,
                                    tzinfo=datetime.timezone.utc),
        )
        track1.user.add(self.user6)

        track2 = TrackParameter.objects.create(
            article='74094837',
            start_at=datetime.datetime(2022, 11, 21, 21, 59,
                                       tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 11, 23, 2, 59,
                                     tzinfo=datetime.timezone.utc),
        )
        track2.user.add(self.user7)

        product1 = Product.objects.create(
            article='74094838',
            brand='adidas',
            name='Кроссовки',
            price_without_discount=999900,
            price_with_discount=739400,
            seller='ВАЙЛДБЕРРИЗ',
            time=datetime.datetime(2022, 4, 23, 2, 59,
                                   tzinfo=datetime.timezone.utc)
        )
        product1.track.add(track1)
        product2 = Product.objects.create(
            article='74094836',
            brand='puma',
            name='Кроссовки',
            price_without_discount=999900,
            price_with_discount=739400,
            seller='ВАЙЛДБЕРРИЗ',
            time=datetime.datetime(2022, 4, 23, 2, 59,
                                   tzinfo=datetime.timezone.utc)
        )
        product2.track.add(track2)
        product3 = Product.objects.create(
            article='74094837',
            brand='puma1',
            name='Кроссовки',
            price_without_discount=999900,
            price_with_discount=739400,
            seller='ВАЙЛДБЕРРИЗ',
            time=datetime.datetime(2022, 4, 23, 2, 59,
                                   tzinfo=datetime.timezone.utc)
        )
        product3.track.add(track1)

        response = self.client.get(reverse('get_user_products'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['article'], product1.article)
        self.assertEqual(response.data['results'][1]['article'], product3.article)


class ProductListForAllTracksViewTest(TestCase):

    def setUp(self):
        self.user8 = get_user_model().objects.create_user(
            'test4@mail.ru',
            'testpass'
        )
        self.user9 = get_user_model().objects.create_user(
            'test5@mail.ru',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user8)

    def test_products_list_for_all_tracks(self):
        track1 = TrackParameter.objects.create(
            article='74094837',
            start_at=datetime.datetime(2022, 12, 21, 21, 59,
                                      tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 12, 23, 2, 59,
                                    tzinfo=datetime.timezone.utc),
        )
        track1.user.add(self.user8)

        track2 = TrackParameter.objects.create(
            article='74094837',
            start_at=datetime.datetime(2022, 11, 21, 21, 59,
                                       tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 11, 23, 2, 59,
                                     tzinfo=datetime.timezone.utc),
        )
        track2.user.add(self.user9)
        track3 = TrackParameter.objects.create(
            article='74094837',
            start_at=datetime.datetime(2022, 11, 21, 21, 59,
                                       tzinfo=datetime.timezone.utc),
            end_at=datetime.datetime(2022, 11, 23, 2, 59,
                                     tzinfo=datetime.timezone.utc),
        )
        track2.user.add(self.user8)

        product1 = Product.objects.create(
            article='74094837',
            brand='adidas',
            name='Кроссовки',
            price_without_discount=999900,
            price_with_discount=739400,
            seller='ВАЙЛДБЕРРИЗ',
            time=datetime.datetime(2022, 4, 23, 2, 59,
                                   tzinfo=datetime.timezone.utc)
        )
        product1.track.add(track1)
        product2 = Product.objects.create(
            article='74094837',
            brand='puma',
            name='Кроссовки',
            price_without_discount=999900,
            price_with_discount=739400,
            seller='ВАЙЛДБЕРРИЗ',
            time=datetime.datetime(2022, 4, 23, 2, 59,
                                   tzinfo=datetime.timezone.utc)
        )
        product2.track.add(track2)
        product3 = Product.objects.create(
            article='74094837',
            brand='puma1',
            name='Кроссовки',
            price_without_discount=999900,
            price_with_discount=739400,
            seller='ВАЙЛДБЕРРИЗ',
            time=datetime.datetime(2022, 4, 23, 2, 59,
                                   tzinfo=datetime.timezone.utc)
        )
        product3.track.add(track3)

        response = self.client.get(reverse('get_product_info', args=[74094837]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['article'], product1.article)
        self.assertEqual(response.data['results'][1]['article'], product3.article)

