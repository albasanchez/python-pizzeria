from django.urls import path
from . import views

urlpatterns = [ 
  path('', views.main, name='main-view'),
  path('register-order', views.registerOrder, name='register-order'),
]
