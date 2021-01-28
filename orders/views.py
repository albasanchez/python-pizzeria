from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from .models import Drink, Ingredient, Size, Client, Order, Delivery, Order_Drink, Pizza, Pizza_Ingredient
from django.db import transaction
from datetime import date

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
    "pizzas": template_pizzas,
    "total_order_price": total_order_price,
  }

  return JsonResponse(response)

@transaction.atomic
def registerOrder(request):
  try:
    data = dict(json.loads(request.body))
    order = data["order"]
    
    pizzas = order["pizzas"]["pizzas"]
    drinks = order["drinks"]["drinks"]
    delivery = order["delivery"]
    client = order["client"]

    #Registro de información del cliente
    registered_client = Client.objects.create(name=client["name"], last_name=client["last_name"], email=client["email"])
    
    #Registro de información de la orden
    registered_order = Order.objects.create(date=date.today(), price=order["total_order_price"], fk_client=registered_client)

    #Registro de información de delivery
    registered_delivery = Delivery.objects.create(price=delivery["price"], fk_order=registered_order, direction=delivery["direction"])

    #Registro de información de las bebidas en la orden
    for drink in drinks:
      fk_drink = Drink.objects.get(pk=drink["id"])
      Order_Drink.objects.create(fk_order=registered_order, fk_drink=fk_drink)
    
    #Registro de información de las pizzas en la orden
    for pizza in pizzas:
      fk_size = Size.objects.get(pk=pizza["size"]["id"])
      registered_pizza = Pizza.objects.create(price=pizza["total_pizza_price"], fk_size=fk_size, fk_order=registered_order)
      for ingredient in pizza["ingredients"]:
        fk_ingredient = Ingredient.objects.get(pk=ingredient["id"])
        Pizza_Ingredient.objects.create(fk_pizza=registered_pizza, fk_ingredient=fk_ingredient)

    return JsonResponse({"status": 200})
  except:
    return JsonResponse({"status": 500})
