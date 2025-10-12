from django.shortcuts import render, redirect
from .models import UserInput
from django.http import HttpResponse

# def Hello(resopnse):
#     return("helloe ")


def main(request):
    return render(request, "main.html")


def input_view(request):
    if request.method == "POST":
         name = request.POST.get("name")
         email = request.POST.get("email")
         password = request.POST.get("password")

         if UserInput.objects.filter(email = email).exists():
            return redirect("failed_page")

         user = UserInput.objects.create(name= name, email = email, password = password)
         return redirect("success", user_id = user.id)

    return render(request, "input.html")




def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get("password")


        try:
            user = UserInput.objects.get(email= email)
            return HttpResponse("WELCOME BACK "+user.name)
        except UserInput.DoesNotExist:
            return redirect('Fail')
    return render(request, 'login.html')   


def fail_view(request):
    return render(request, 'failregistration.html') 

def fail(request):
    return render(request, 'faillogin.html')

def success_view(request, user_id):
    user = UserInput.objects.get(id =user_id)
    return render(request, "success.html", {"user": user})
