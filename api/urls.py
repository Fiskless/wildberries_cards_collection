from django.urls import path, include
from api.views import TrackParameterCreateView, TrackParameterVListView, \
    ProductListView, ProductsListView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('user/track_create/', TrackParameterCreateView.as_view()),
    path('user/tracks/', TrackParameterVListView.as_view()),
    path('user/products/', ProductsListView.as_view()),
    path('user/product/<int:article>/', ProductListView.as_view())
]