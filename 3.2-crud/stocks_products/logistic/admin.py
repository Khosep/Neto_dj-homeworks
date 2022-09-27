from django.contrib import admin
from .models import StockProduct, Product, Stock

class StockProductInline(admin.TabularInline):
    model = StockProduct
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']


@admin.register(Stock)
class Stock(admin.ModelAdmin):
    list_display = ['address']
    inlines = [StockProductInline]