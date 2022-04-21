import datetime

from django.utils.timezone import utc
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.serializers import TrackParameterSerializer, ProductListSerializer
from cards.models import TrackParameter, Product
from django_filters import rest_framework as filters


class ProductListFilter(filters.FilterSet):
    articles = filters.CharFilter(method='get_products_by_articles',
                                      label='Укажите через запятую артикулы товаров, которые хотите отслеживать')

    def get_products_by_articles(self, value, queryset, name, ):
        articles = name.split(',')
        products = Product.objects.filter(article__in=articles)
        return products

    class Meta:
        model = Product
        fields = ['articles']


class TrackParameterListFilter(filters.FilterSet):

    class Meta:
        model = Product
        fields = ['time_interval', 'start_at', 'end_at']


class TrackParameterCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackParameterSerializer


class TrackParameterListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackParameterSerializer

    def get_queryset(self):
        return TrackParameter.objects.filter(user=self.request.user)


class TrackParameterDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackParameterSerializer

    def get_object(self):
        track = TrackParameter.\
            objects.\
            filter(id=self.kwargs['pk']).\
            filter(start_at__gte=datetime.datetime.utcnow().replace(tzinfo=utc)).\
            first()
        return track


class ProductsForTrackParameterListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        tracks = TrackParameter.\
            objects.\
            filter(id=self.kwargs['pk']).\
            prefetch_related('products').first()
        return tracks.products.all()


class ProductsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductListFilter

    def get_queryset(self):
        tracks = TrackParameter.objects.filter(user=self.request.user)
        return Product.objects.filter(track__in=tracks)


class ProductListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        tracks = TrackParameter.objects.filter(user=self.request.user)
        return Product.\
            objects.\
            filter(track__in=tracks).\
            filter(article=self.kwargs['article'])