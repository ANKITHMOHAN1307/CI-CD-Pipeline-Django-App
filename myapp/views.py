<<<<<<< HEAD
from django.shortcuts import HttpResponse

def Hello(request):
    return HttpResponse("Hello from django !")
=======
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello from myapp in myprojct")
>>>>>>> 91b95fe (First CI test)
