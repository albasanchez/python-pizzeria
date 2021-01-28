from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from .models import Drink, Ingredient, Size
import json

def main(request):
  template = loader.get_template("orders/index.html")
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
    template_ingredients.append({"id": ingredient.id, "name": ingredient.name, "price": ingredient.price})
  
  for size in sizes:
    template_sizes.append({"id": size.id, "name": size.name, "price": size.price})
  
  for drink in drinks:
    template_drinks.append({"id": drink.id, "name": drink.name, "price": drink.price})

  context = {
    "ingredients": template_ingredients,
    "sizes": template_sizes,
    "drinks": template_drinks
  }

  return HttpResponse(template.render(context, request))      

def calculateOrder(request):
  data = dict(json.loads(request.body))
  order = data["order"]
  
  pizzas = order["pizzas"]
  drinks = order["drinks"]
  delivery = order["delivery"]

  total_order_price = 0
  total_pizzas = 0
  total_drinks = 0
  total_delivery = delivery["price"]

  template_drinks = {"drinks": drinks, "total": len(drinks), "total_drinks_price": 0}
  template_delivery = {"price": delivery["price"], "direction": delivery["direction"]}
  template_pizzas = {"pizzas": [], "total": len(pizzas), "total_pizzas_price": 0}

  #Cálculo del costo de las pizzas
  for pizza in pizzas:
    total_pizza_price = 0
    total_pizza_price = total_pizza_price + pizza["size"]["price"]

    for ingredient in pizza["ingredients"]:
      total_pizza_price = total_pizza_price + ingredient["price"]
    
    template_pizzas["pizzas"].append({"total_pizza_price": total_pizza_price, "size": pizza["size"], "ingredients": pizza["ingredients"]})
    total_pizzas = total_pizzas + total_pizza_price
  
  template_pizzas["total_pizzas_price"] = total_pizzas
  
  #Cálculo del costo de las bebidas
  for drink in drinks:
    total_drinks = total_drinks + drink["price"]

  template_drinks["total_drinks_price"] = total_drinks

  #Cálculo del costo total de la orden
  total_order_price = total_delivery + total_drinks + total_pizzas

  response = {
    "drinks": template_drinks,
    "delivery": template_delivery,
    "pizzas": template_pizzas
  }

  return JsonResponse(response)

def registerOrder(request):
  data = json.loads(request.body)
  print(data)
  print(data["order"])
  return HttpResponse(data["order"])
