from django.urls import path
from . import views

urlpatterns = [
    # path('', views.Hello, name = 'Hello'),
    path('', views.input_view, name = 'input'),
    path('success/<int:user_id>/', views.success_view, name ='success'),
]   
# sucess_view