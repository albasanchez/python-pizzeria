from django.contrib import admin
from django.db.models import Count

from .models import Client, Order, Size, Ingredient, Pizza, Pizza_Ingredient, Drink, Order_Drink, Delivery

def custom_titled_filter(title):
    '''
        Se define una clase Wrapper con la finalidad de agregar
        un titulo personalizado a las distintas columnas que poseen
        los modelos en la zona administrativa.
    '''
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class OrderAdmin(admin.ModelAdmin):
    '''
        Clase que permite definir la configuracion de que, como y cuales datos se muestran
        en la zona administrativa, correspondiente al modelo "Order". Tambien es donde se
        definen los filtros para aplicar a los datos en la zona administrativa.
    '''
    list_display = ('id', 'client', 'price', 'date', 'pizzas', 'drinks', 'delivery')
    list_filter = (
        ('date', custom_titled_filter('Fecha')),
        ('pizza__fk_size__name', custom_titled_filter('Tamaño de pizza')),
        ('pizza__pizza_ingredient__fk_ingredient__name', custom_titled_filter('Ingrediente')),
        ('fk_client__email', custom_titled_filter('Cliente'))
    )

class PizzaAdmin(admin.ModelAdmin):
    '''
        Clase que permite definir la configuracion de que, como y cuales datos se muestran
        en la zona administrativa, correspondiente al modelo "Pizza".
    '''
    list_display = ('fk_order', 'orderPrice', 'fk_size', 'price')

class IngredientAdmin(admin.ModelAdmin):
    '''
        Clase que permite definir la configuracion de que, como y cuales datos se muestran
        en la zona administrativa, correspondiente al modelo "Ingredient". Tambien es donde se
        definen los filtros para aplicar a los datos en la zona administrativa.
    '''
    list_display = ('name', 'price', 'order', 'totalOrderPrice')
    list_filter = ('name',)

class ClientAdmin(admin.ModelAdmin):
    '''
        Clase que permite definir la configuracion de que, como y cuales datos se muestran
        en la zona administrativa, correspondiente al modelo "Client". Tambien es donde se
        definen los filtros para aplicar a los datos en la zona administrativa. Se define
        el metodo totalOrderPrices para poder sortear los datos dependiendo de la orden.
    '''
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
    '''
        Clase que permite definir la configuracion de que, como y cuales datos se muestran
        en la zona administrativa, correspondiente al modelo "Size". Tambien es donde se
        definen los filtros para aplicar a los datos en la zona administrativa.
    '''
    list_display = ('name', 'order', 'totalOrderPrice')
    list_filter = ('name',)

'''
    Se registran los modelos en la zona administrativa y se asocian con su respectiva clase
'''
admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Pizza_Ingredient)
admin.site.register(Drink)
admin.site.register(Order_Drink)
admin.site.register(Delivery)
