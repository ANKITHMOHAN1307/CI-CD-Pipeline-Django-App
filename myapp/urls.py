from django.urls import path
from . import views

urlpatterns = [
    # path('', views.Hello, name = 'Hello'),
    path('', views.main, name = "maingpage"),
    path('login/', views.login_view, name = 'login'),
    path('input/', views.input_view, name = 'register'),
    path('success_view/<int:user_id>/', views.success_view, name ='success'),
    path('fail_view/', views.fail_view, name = "failed_page"),
    path('fail/', views.fail, name = "Fail")

]   
# 