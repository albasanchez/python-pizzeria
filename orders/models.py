from django.db import models

class Client(models.Model):
  name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  email = models.EmailField()

  def __str__(self):
    return self.name + ' ' + self.last_name
  
class Order(models.Model):
  date = models.DateTimeField()
  price = models.FloatField(default=0)
  fk_client = models.ForeignKey(Client, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.id)

# Pizza
class Size(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

  def __str__(self):
    return self.name

class Ingredient(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

  def __str__(self):
    return self.name

class Pizza(models.Model):
  price = models.FloatField(default=0)
  fk_size = models.ForeignKey(Size, on_delete=models.CASCADE)
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.id)

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
