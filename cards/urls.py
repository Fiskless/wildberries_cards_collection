from django.urls import path
from .views import login_view, register_view, logout_view, create_product_track


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('track_parameters/', create_product_track, name='track_parameters')
]