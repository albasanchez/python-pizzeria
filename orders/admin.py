from django.contrib import admin

from .models import Client, Order, Size, Ingredient, Pizza, Pizza_Ingredient, Drink, Order_Drink, Delivery

'''
class OrderBySizeListFilter(admin.SimpleListFilter):
    title = ('Size')
    parameter_name = 'TamanoPizza'

    def lookups(self, request, model_admin):
        return (
            ('G', ('Grande')),
            ('M', ('Mediana')),
            ('P', ('Pequena')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'G':
            return queryset.filter()
        if self.value() == 'M':
            return queryset.filter()
        if self.value() == 'P':
            return queryset.filter()
'''

class OrderAdmin(admin.ModelAdmin):
    list_display = ('price', 'date', 'Cliente')
    #list_filter = (OrderBySizeListFilter,)

admin.site.register(Client)
admin.site.register(Order, OrderAdmin)
admin.site.register(Size)
admin.site.register(Ingredient)
admin.site.register(Pizza)
admin.site.register(Pizza_Ingredient)
admin.site.register(Drink)
admin.site.register(Order_Drink)
admin.site.register(Delivery)

# Register your models here.
