from django.db import models
import datetime

class Client(models.Model):
  name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  email = models.EmailField(unique=True)

  def __str__(self):
    return self.name + ' ' + self.last_name
  
  def order(self):
    orders = Order.objects.all()
    orderList = []
    for order in orders:
      if order.fk_client.id == self.id:
        orderList.append(order)
    return orderList
  
  def totalOrderPrice(self):
    orders = Order.objects.all()
    orderPrice = 0
    for order in orders:
      if order.fk_client.id == self.id:
        orderPrice = orderPrice + order.price
    return orderPrice
  
class Order(models.Model):
  date = models.DateField(auto_now=True)
  price = models.FloatField(default=0)
  fk_client = models.ForeignKey(Client, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.id)

  def Cliente(self):
    return self.fk_client.name + ' ' + self.fk_client.last_name

# Pizza
class Size(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

  def __str__(self):
    return self.name
  
  def order(self):
    pizzas = Pizza.objects.all()
    orders = Order.objects.all()
    orderList= []
    for pizza in pizzas:
      if pizza.fk_size.id == self.id:
        for order in orders:
          if pizza.fk_order.id == order.id:
            orderList.append(order)
    return orderList

  def totalOrderPrice(self):
    pizzas = Pizza.objects.all()
    orders = Order.objects.all()
    orderPrice = 0
    for pizza in pizzas:
      if pizza.fk_size.id == self.id:
        for order in orders:
          if pizza.fk_order.id == order.id:
            orderPrice = orderPrice + order.price
    return orderPrice 

class Ingredient(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

  def __str__(self):
    return self.name

  def order(self):
    pizzas = Pizza.objects.all()
    pizzaIng = Pizza_Ingredient.objects.all()
    orderList = []
    for pi in pizzaIng:
      if pi.fk_ingredient.id == self.id:
        for pizza in pizzas:
          if pizza.id == pi.fk_pizza.id:
            orderList.append(pizza.fk_order)
    return orderList
  
  def totalOrderPrice(self):
    pizzas = Pizza.objects.all()
    pizzaIng = Pizza_Ingredient.objects.all()
    orderPrice = 0
    for pi in pizzaIng:
      if pi.fk_ingredient.id == self.id:
        for pizza in pizzas:
          if pizza.id == pi.fk_pizza.id:
            orderPrice = orderPrice + pizza.fk_order.price
    return orderPrice

class Pizza(models.Model):
  price = models.FloatField(default=0)
  fk_size = models.ForeignKey(Size, on_delete=models.CASCADE)
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.id)
  
  def orderPrice(self):
    orders = Order.objects.all()
    for order in orders:
      if order.id == self.fk_order.id:
        return order.price

class Pizza_Ingredient(models.Model):
  fk_pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
  fk_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.fk_pizza)

# Drink
class Drink(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

  def __str__(self):
    return self.name

class Order_Drink(models.Model):
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)
  fk_drink = models.ForeignKey(Drink, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.id)

# Delivery
class Delivery(models.Model):
  direction = models.CharField(max_length=1000)
  price = models.FloatField(default=0)
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.id) + ' - ' + self.direction