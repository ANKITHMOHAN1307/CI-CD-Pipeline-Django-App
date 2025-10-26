from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.Hello, name = 'Hello')
]
=======
    path("", views.hello_world, name="hello_world"),
]
>>>>>>> 91b95fe (First CI test)
