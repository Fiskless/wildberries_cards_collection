from django.urls import path, include
from api.views import TrackParameterCreateView, TrackParameterVListView, \
    ProductListView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('user/track_create/', TrackParameterCreateView.as_view()),
    path('user/tracks/', TrackParameterVListView.as_view()),
    path('user/products/', ProductListView.as_view())
]