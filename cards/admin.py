from django.contrib import admin
from .models import Product, TrackParameter


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['time']
    pass


@admin.register(TrackParameter)
class TrackParameterAdmin(admin.ModelAdmin):
    pass