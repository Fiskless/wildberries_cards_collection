from django.urls import path, include
from api.views import TrackParameterCreateView, TrackParameterVListView, \
    ProductListView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]