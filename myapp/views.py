from django.shortcuts import HttpResponse

def Hello(request):
    return HttpResponse("Hello from django !")