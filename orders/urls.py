from django.urls import path
from . import views

urlpatterns = [ 
  path('', views.main, name='main-view'),
  path('calculate-order', views.calculateOrder, name='calculate-order'),
  path('register-order', views.registerOrder, name='register-order'),
]
