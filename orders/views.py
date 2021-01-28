from django.http import HttpResponse, Http404
from django.template import loader
from .models import Drink, Ingredient, Size
import json

def main(request):
  template = loader.get_template('orders/index.html')
  try:
    ingredients = Ingredient.objects.all()
    sizes = Size.objects.all()
    drinks = Drink.objects.all()
  except:
    raise Http404("Fallo al obtener la información base!")

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

def registerOrder(request):
  data = json.loads(request.body)
  print(data)
  print(data["order"])
  return HttpResponse(data["order"])