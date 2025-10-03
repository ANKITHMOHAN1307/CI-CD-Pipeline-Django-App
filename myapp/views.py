from django.shortcuts import render, redirect
from .forms import UserInput
from .models import UserInput

# def Hello(resopnse):
#     return("helloe ")


def input_view(request):
    if request.method == "POST":
         name = request.POST.get("name")
         email = request.POST.get("email")

         user = UserInput.objects.create(name= name, email = email)

         return redirect("success", user_id = user.id)

    return render(request, "input.html")
def success_view(request, user_id):
    user = UserInput.objects.get(id =user_id)
    return render(request, "success.html", {"user": user})


