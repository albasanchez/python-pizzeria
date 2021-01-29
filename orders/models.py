from django.db import models
import datetime

"""
  Usuarios de la aplicación web, aquellos que realizan las órdenes
"""
class Client(models.Model):
  name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  email = models.EmailField(unique=True)

  """
    Usado para obtener una representación personalizada del objeto cliente
  """
  def __str__(self):
    return self.name + ' ' + self.last_name
  
  """
    Usado para visualizar en el apartado administrativo
    Obtiene el listado de los identificadores de las ordenes realizadas por el cliente
  """
  def order(self):
    orders = Order.objects.all()
    orderList = []
    for order in orders:
      if order.fk_client.id == self.id:
        orderList.append(order)
    return orderList
  
  """
    Usado para visualizar en el apartado administrativo
    Obtiene el precio total de todas las ordenes realizadas por el cliente
  """
  def totalOrderPrice(self):
    orders = Order.objects.all()
    orderPrice = 0
    for order in orders:
      if order.fk_client.id == self.id:
        orderPrice = orderPrice + order.price
    return orderPrice

"""
  Pedidos que se elaboran dentro de la pizzeria
"""
class Order(models.Model):
  date = models.DateField(auto_now=True)
  price = models.FloatField(default=0)
  fk_client = models.ForeignKey(Client, on_delete=models.CASCADE)

  """
    Usado para obtener una representación personalizada del objeto orden
  """
  def __str__(self):
    return str(self.id)

  """
    Usado para visualizar en el apartado administrativo
    Obtiene el nombre del cliente asociado a la orden
  """
  def client(self):
    return self.fk_client.name + ' ' + self.fk_client.last_name

  """
    Usado para visualizar en el apartado administrativo
    Obtiene la cantidad de pizzas asociadas a la orden
  """
  def pizzas(self):
    pizzas = Pizza.objects.filter(fk_order = self).count()
    return pizzas

  """
    Usado para visualizar en el apartado administrativo
    Obtiene la cantidad de bebidas asociadas a la orden
  """
  def drinks(self):
    drinks = Order_Drink.objects.filter(fk_order = self).count()
    return drinks

  """
    Usado para visualizar en el apartado administrativo
    Obtiene si existe un delivery asociado a la orden
  """
  def delivery(self):
    delivery = Delivery.objects.filter(fk_order=self).count()
    return delivery==1
  
  delivery.boolean = True

"""
  Tamaño de la pizza. Ya sea Grande, Mediana o Personal
"""
class Size(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

  """
    Usado para obtener una representación personalizada del objeto tamaño
  """
  def __str__(self):
    return self.name
  
  """
    Usado para visualizar en el apartado administrativo
    Obtiene el listado de los identificadores de las ordenes que contienen el tamaño de pizza
  """
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

  """
    Usado para visualizar en el apartado administrativo
    Obtiene el precio total de todas las ordenes que contienen el tamaño de pizza
  """
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

"""
  Ingredientes que se agregan a una pizza
"""
class Ingredient(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

  """
    Usado para obtener una representación personalizada del objeto ingrediente
  """
  def __str__(self):
    return self.name

  """
    Usado para visualizar en el apartado administrativo
    Obtiene el listado de los identificadores de las ordenes que contienen el ingrediente
  """
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

  """
    Usado para visualizar en el apartado administrativo
    Obtiene el precio total de todas las ordenes que contienen el ingrediente
  """
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

"""
  Corresponde a cada pizza que se pide en una orden
"""
class Pizza(models.Model):
  price = models.FloatField(default=0)
  fk_size = models.ForeignKey(Size, on_delete=models.CASCADE)
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)

  """
    Usado para obtener una representación personalizada del objeto pizza
  """
  def __str__(self):
    return str(self.id)

  """
    Usado para visualizar en el apartado administrativo
    Obtiene el precio de todas la orden que contiene la pizza
  """
  def orderPrice(self):
    orders = Order.objects.all()
    for order in orders:
      if order.id == self.fk_order.id:
        return order.price

"""
  Se crea a partir de la relación muchos a muchos entre la tabla Pizza y la tabla Ingrediente,
  ya que una pizza puede tener muchos ingredientes y un ingrediente puede estar en muchas pizzas
"""
class Pizza_Ingredient(models.Model):
  fk_pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
  fk_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

  """
    Usado para obtener una representación personalizada del objeto pizza_ingrediente
  """
  def __str__(self):
    return str(self.fk_pizza)

"""
  Corresponde a cada bebida que se pide en una orden
"""
class Drink(models.Model):
  name = models.CharField(max_length=200)
  price = models.FloatField(default=0)

  """
    Usado para obtener una representación personalizada del objeto bebida
  """
  def __str__(self):
    return self.name

"""
  Se crea a partir de la relación muchos a muchos entre la tabla Orden y la tabla Bebida,
  ya que una orden puede tener muchas bebidas y una bebida puede estar en muchas órdenes
"""
class Order_Drink(models.Model):
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)
  fk_drink = models.ForeignKey(Drink, on_delete=models.CASCADE)

  """
    Usado para obtener una representación personalizada del objeto orden_bebida
  """
  def __str__(self):
    return str(self.id)

"""
  Utilizado para almacenar el envío de la orden en caso de que se desee
"""
class Delivery(models.Model):
  direction = models.CharField(max_length=1000)
  price = models.FloatField(default=0)
  fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)

  """
    Usado para obtener una representación personalizada del objeto delivery
  """
  def __str__(self):
    return str(self.id) + ' - ' + self.direction