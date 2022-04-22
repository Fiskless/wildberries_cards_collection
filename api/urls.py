from django.urls import path, include
from api.views import TrackParameterCreateView, TrackParameterListView, \
    ProductListView, ProductsListView, TrackParameterDetailView, \
    ProductsForTrackParameterListView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('user/track_create/', TrackParameterCreateView.as_view(), name='create_new_track'),
    path('user/tracks/', TrackParameterListView.as_view(), name='get_all_tracks'),
    path('user/track/<int:pk>/', TrackParameterDetailView.as_view(), name='get_track'),
    path('user/track/<int:pk>/products/', ProductsForTrackParameterListView.as_view(), name='get_track_products'),
    path('user/products/', ProductsListView.as_view(), name='get_user_products'),
    path('user/product/<int:article>/', ProductListView.as_view(), name='get_product_info')
]