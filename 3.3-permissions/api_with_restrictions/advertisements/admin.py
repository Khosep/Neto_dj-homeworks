from django.contrib import admin
from .models import Advertisement, Favorites


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'status', 'creator', 'created_at', 'updated_at']

@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'user', 'advert']
    ordering = ['user_id']

