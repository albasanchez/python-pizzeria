from django.http import HttpResponse
from django.template import loader

import json

def index(request):
  template = loader.get_template('orders/index.html')
  items = ['Queso', 'Fruta', 'Chocolate', 'Helado', 'Ropa', 'Zapatos']
  context = {
    'int_data': 3,
    'str_data': 'Hola, esta es una prueba de string',
    'array_data': items,
  }
  return HttpResponse(template.render(context, request))

def test(request):
  template = loader.get_template('orders/test.html')
  return HttpResponse(template.render({}, request))
