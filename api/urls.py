from django.urls import path, include
from api.views import TrackParameterCreateView, TrackParameterListView, \
    ProductListView, ProductsListView, TrackParameterDetailView, \
    ProductsForTrackParameterListView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('user/track_create/', TrackParameterCreateView.as_view()),
    path('user/tracks/', TrackParameterListView.as_view()),
    path('user/track/<int:pk>/', TrackParameterDetailView.as_view()),
    path('user/track/<int:pk>/products/', ProductsForTrackParameterListView.as_view()),
    path('user/products/', ProductsListView.as_view()),
    path('user/product/<int:article>/', ProductListView.as_view())
]