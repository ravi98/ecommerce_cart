from django.urls import path
from . import views

app_name='social'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('register/', views.UserRegistration.as_view(), name="user_registration"),
    path('login/', views.UserLogin.as_view(), name="user_login"),
    path('logout/', views.custom_logout, name="user_logout"),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_details, name='product_detail'),
]
