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

  def Cliente(self):
    return self.fk_client.name + ' ' + self.fk_client.last_name
  
  def TamanoPizza(self):
    pizzas = Pizza.objects.all()
    for pizza in pizzas:
      if pizza.fk_order.id == self.id:
        return pizza.fk_size

  def Ingredientes(self):
    ingredientes = Ingredient.objects.all()
    pizzas = Pizza.objects.all()
    pizzaIng = Pizza_Ingredient.objects.all()
    ingredients = []
    for pizza in pizzas:
      if pizza.fk_order.id == self.id:
        for pi in pizzaIng:
          if pizza.id == pi.fk_pizza.id:
            ingredients.append(pi.fk_ingredient.name)
        
    return ingredients

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
