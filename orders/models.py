from django.db import models

class Client(models.Model):
  name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  email = models.EmailField()
  
class Order(models.Model):
  date = models.DateTimeField()
  price = models.FloatField(default=0)
  fk_client = models.ForeignKey(Client, on_delete=models.CASCADE)

# Pizza
class Size(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

class Ingredient(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

class Pizza(models.Model):
  price = models.FloatField(default=0)
  fk_size = models.ForeignKey(Size, on_delete=models.CASCADE)
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Pizza_Ingredient(models.Model):
  fk_pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
  fk_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

# Drink
class Drink(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

class Order_Drink(models.Model):
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)
  fk_drink = models.ForeignKey(Drink, on_delete=models.CASCADE)

# Delivery
class Delivery(models.Model):
  direction = models.CharField(max_length=1000)
  price = models.FloatField(default=0)
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)
