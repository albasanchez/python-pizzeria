from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from .models import Drink, Ingredient, Size, Client, Order, Delivery, Order_Drink, Pizza, Pizza_Ingredient
from django.db import transaction
from django.utils import timezone
from datetime import date

import json


"""
Esta vista corresponde a la página donde se realiza el proceso de pedido.
-Obtiene la información de los ingredientes, bebidas y tamaños de pizza
-Renderiza el template de index.html
"""
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

"""
Esta vista corresponde al cálculo de la orden.
-Calcula el total por cada pizza.
-Calcula el total de la orden sumando el total de las pizzas, las bebidas y el delivery.
"""
def calculateOrder(request):
  data = dict(json.loads(request.body))
  order = data["order"]
  
  pizzas = order["pizzas"]
  drinks = order["drinks"]
  delivery = order["delivery"]

  total_order_price = 0
  total_pizzas = 0
  total_drinks = 0

  if delivery["direction"] == "":
    total_delivery = 0
  else:
    total_delivery = float("{0:.2f}".format(delivery["price"]))

  template_drinks = {"drinks": drinks, "total": len(drinks), "total_drinks_price": 0}
  template_delivery = {"price": total_delivery, "direction": delivery["direction"]}
  template_pizzas = {"pizzas": [], "total": len(pizzas), "total_pizzas_price": 0}

  #Cálculo del costo de las pizzas
  for pizza in pizzas:
    total_pizza_price = 0
    total_pizza_price = total_pizza_price + pizza["size"]["price"]

    for ingredient in pizza["ingredients"]:
      total_pizza_price = total_pizza_price + ingredient["price"]
    
    template_pizzas["pizzas"].append({"total_pizza_price": float("{0:.2f}".format(total_pizza_price)), "size": pizza["size"], "ingredients": pizza["ingredients"]})
    total_pizzas = total_pizzas + total_pizza_price
  
  template_pizzas["total_pizzas_price"] = float("{0:.2f}".format(total_pizzas))
  
  #Cálculo del costo de las bebidas
  for drink in drinks:
    total_drinks = total_drinks + drink["price"]

  template_drinks["total_drinks_price"] = float("{0:.2f}".format(total_drinks))

  #Cálculo del costo total de la orden
  total_order_price = float("{0:.2f}".format(total_delivery + total_drinks + total_pizzas))

  response = {
    "drinks": template_drinks,
    "delivery": template_delivery,
    "pizzas": template_pizzas,
    "total_order_price": total_order_price,
  }

  return JsonResponse(response)

"""
Esta vista corresponde al registro de la orden.
-Registro de toda la información correspondiente a la orden.
-Se hace uso de transacciones en caso de errores.
"""
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
    registered_client = None
    email_exist = Client.objects.filter(email = client["email"]).count()
    if email_exist > 0:
      registered_client = Client.objects.get(email = client["email"])
    else:
      registered_client = Client.objects.create(name=client["name"], last_name=client["last_name"], email=client["email"])
    
    #Registro de información de la orden
    registered_order = Order.objects.create(price=order["total_order_price"], fk_client=registered_client)

    #Registro de información de delivery
    if delivery["price"] != 0 and delivery["direction"] != "":
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
  except err:
    print(err)
    return JsonResponse({"status": 500})
