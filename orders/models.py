from django.db import models
import datetime


class Client(models.Model):
  """
    Usuarios de la aplicación web, aquellos que realizan las órdenes
  """
  name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  email = models.EmailField(unique=True)


  def __str__(self):
  """
    Usado para obtener una representación personalizada del objeto cliente
  """
    return self.name + ' ' + self.last_name
  
  def order(self):
  """
    Usado para visualizar en el apartado administrativo
    Obtiene el listado de los identificadores de las ordenes realizadas por el cliente
  """
    orders = Order.objects.all()
    orderList = []
    for order in orders:
      if order.fk_client.id == self.id:
        orderList.append(order)
    return orderList
  
  def totalOrderPrice(self):
  """
    Usado para visualizar en el apartado administrativo
    Obtiene el precio total de todas las ordenes realizadas por el cliente
  """
    orders = Order.objects.all()
    orderPrice = 0
    for order in orders:
      if order.fk_client.id == self.id:
        orderPrice = orderPrice + order.price
    return orderPrice


class Order(models.Model):
  """
    Pedidos que se elaboran dentro de la pizzeria
  """
  date = models.DateField(auto_now=True)
  price = models.FloatField(default=0)
  fk_client = models.ForeignKey(Client, on_delete=models.CASCADE)

  def __str__(self):
  """
    Usado para obtener una representación personalizada del objeto orden
  """
    return str(self.id)

  def client(self):
  """
    Usado para visualizar en el apartado administrativo
    Obtiene el nombre del cliente asociado a la orden
  """
    return self.fk_client.name + ' ' + self.fk_client.last_name

  def pizzas(self):
  """
    Usado para visualizar en el apartado administrativo
    Obtiene la cantidad de pizzas asociadas a la orden
  """
    pizzas = Pizza.objects.filter(fk_order = self).count()
    return pizzas

  def drinks(self):
  """
    Usado para visualizar en el apartado administrativo
    Obtiene la cantidad de bebidas asociadas a la orden
  """
    drinks = Order_Drink.objects.filter(fk_order = self).count()
    return drinks

  def delivery(self):
  """
    Usado para visualizar en el apartado administrativo
    Obtiene si existe un delivery asociado a la orden
  """
    delivery = Delivery.objects.filter(fk_order=self).count()
    return delivery==1
  
  delivery.boolean = True

class Size(models.Model):
"""
  Tamaño de la pizza. Ya sea Grande, Mediana o Personal
"""
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

  def __str__(self):
  """
    Usado para obtener una representación personalizada del objeto tamaño
  """
    return self.name
  
  def order(self):
  """
    Usado para visualizar en el apartado administrativo
    Obtiene el listado de los identificadores de las ordenes que contienen el tamaño de pizza
  """
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
  """
    Usado para visualizar en el apartado administrativo
    Obtiene el precio total de todas las ordenes que contienen el tamaño de pizza
  """
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
"""
  Ingredientes que se agregan a una pizza
"""
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

  def __str__(self):
  """
    Usado para obtener una representación personalizada del objeto ingrediente
  """
    return self.name

  def order(self):
  """
    Usado para visualizar en el apartado administrativo
    Obtiene el listado de los identificadores de las ordenes que contienen el ingrediente
  """
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
  """
    Usado para visualizar en el apartado administrativo
    Obtiene el precio total de todas las ordenes que contienen el ingrediente
  """
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
"""
  Corresponde a cada pizza que se pide en una orden
"""
  price = models.FloatField(default=0)
  fk_size = models.ForeignKey(Size, on_delete=models.CASCADE)
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)

  def __str__(self):
  """
    Usado para obtener una representación personalizada del objeto pizza
  """
    return str(self.id)

  def orderPrice(self):
  """
    Usado para visualizar en el apartado administrativo
    Obtiene el precio de todas la orden que contiene la pizza
  """
    orders = Order.objects.all()
    for order in orders:
      if order.id == self.fk_order.id:
        return order.price

class Pizza_Ingredient(models.Model):
"""
  Se crea a partir de la relación muchos a muchos entre la tabla Pizza y la tabla Ingrediente,
  ya que una pizza puede tener muchos ingredientes y un ingrediente puede estar en muchas pizzas
"""
  fk_pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
  fk_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

  def __str__(self):
  """
    Usado para obtener una representación personalizada del objeto pizza_ingrediente
  """
    return str(self.fk_pizza)

class Drink(models.Model):
"""
  Corresponde a cada bebida que se pide en una orden
"""
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

  def __str__(self):
  """
    Usado para obtener una representación personalizada del objeto bebida
  """
    return self.name

class Order_Drink(models.Model):
"""
  Se crea a partir de la relación muchos a muchos entre la tabla Orden y la tabla Bebida,
  ya que una orden puede tener muchas bebidas y una bebida puede estar en muchas órdenes
"""
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)
  fk_drink = models.ForeignKey(Drink, on_delete=models.CASCADE)

  def __str__(self):
  """
    Usado para obtener una representación personalizada del objeto orden_bebida
  """
    return str(self.id)

class Delivery(models.Model):
"""
  Utilizado para almacenar el envío de la orden en caso de que se desee
"""
  direction = models.CharField(max_length=1000)
  price = models.FloatField(default=0)
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)

  def __str__(self):
  """
    Usado para obtener una representación personalizada del objeto delivery
  """
    return str(self.id) + ' - ' + self.direction