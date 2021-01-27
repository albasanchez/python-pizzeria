from django.http import HttpResponse

def index(request):
  return HttpResponse("Hola UCAB. Usted está en el índice de orders")
