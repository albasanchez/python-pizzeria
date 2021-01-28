from django.contrib import admin

from .models import Client, Order, Size, Ingredient, Pizza, Pizza_Ingredient, Drink, Order_Drink, Delivery

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'date', 'Cliente')
    list_filter = ('date', )

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_order', 'orderPrice', 'fk_size', 'price')
    list_filter = ('fk_size',)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'order', 'totalOrderPrice')
    list_filter = ('name',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'order', 'totalOrderPrice')
    list_filter = ('name', 'last_name')

admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Size)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Pizza_Ingredient)
admin.site.register(Drink)
admin.site.register(Order_Drink)
admin.site.register(Delivery)

# Register your models here.
