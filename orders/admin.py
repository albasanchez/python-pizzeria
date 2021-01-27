from django.contrib import admin

from .models import Client, Order, Size, Ingredient, Pizza, Pizza_Ingredient, Drink, Order_Drink, Delivery

admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Size)
admin.site.register(Ingredient)
admin.site.register(Pizza)
admin.site.register(Pizza_Ingredient)
admin.site.register(Drink)
admin.site.register(Order_Drink)
admin.site.register(Delivery)

# Register your models here.
