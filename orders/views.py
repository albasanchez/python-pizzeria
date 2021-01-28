from django.http import HttpResponse
from django.template import loader
from .models import Drink, Ingredient, Size

import json

def main(request):
  if request.method == 'POST':
    return HttpResponse("Test POST")
  
  if request.method == 'GET':
    template = loader.get_template('orders/index.html')
    ingredients = Ingredient.objects.all()
    sizes = Size.objects.all()
    drinks = Drink.objects.all()

    template_ingredients = []
    template_sizes = []
    template_drinks = []

    for ingredient in ingredients:
      template_ingredients.append({'id': ingredient.id, 'name': ingredient.name, 'price': ingredient.price})
    
    for size in sizes:
      template_sizes.append({'id': size.id, 'name': size.name, 'price': size.price})
    
    for drink in drinks:
      template_drinks.append({'id': drink.id, 'name': drink.name, 'price': drink.price})

    context = {
      'ingredients': template_ingredients,
      'sizes': template_sizes,
      'drinks': template_drinks
    }

    return HttpResponse(template.render(context, request))      
