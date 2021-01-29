from django.contrib import admin
from django.db.models import Count

from .models import Client, Order, Size, Ingredient, Pizza, Pizza_Ingredient, Drink, Order_Drink, Delivery

def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'price', 'date', 'pizzas', 'drinks', 'delivery')
    list_filter = (
        ('date', custom_titled_filter('Fecha')),
        ('pizza__fk_size__name', custom_titled_filter('Tamaño de pizza')),
        ('pizza__pizza_ingredient__fk_ingredient__name', custom_titled_filter('Ingrediente')),
        ('fk_client__email', custom_titled_filter('Cliente'))
    )

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('fk_order', 'orderPrice', 'fk_size', 'price')

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'order', 'totalOrderPrice')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'email', 'order', 'totalOrderPrices')
    list_filter = ('name', 'last_name')

    def totalOrderPrices(self, obj):
        orders = Order.objects.all()
        orderPrice = 0
        for order in orders:
            if order.fk_client.id == obj.id:
                orderPrice = orderPrice + order.price
        return orderPrice
    
    totalOrderPrices.admin_order_field = 'name'

class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'totalOrderPrice')

admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Pizza_Ingredient)
admin.site.register(Drink)
admin.site.register(Order_Drink)
admin.site.register(Delivery)

# Register your models here.
