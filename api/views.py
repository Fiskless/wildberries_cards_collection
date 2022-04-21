import django_filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.serializers import TrackParameterSerializer, ProductListSerializer
from cards.models import TrackParameter, Product
from django_filters import rest_framework as filters


class ProductListFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="start_at", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="end_at", lookup_expr='lte')


class TrackParameterCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackParameterSerializer


class TrackParameterVListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackParameterSerializer

    def get_queryset(self):
        return TrackParameter.objects.filter(user=self.request.user)


class ProductListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductListFilter

    def get_queryset(self):
        tracks = TrackParameter.objects.filter(user=self.request.user)
        return Product.objects.filter(track__in=tracks)

