from django.urls import path
from . import views

app_name="orders"

urlpatterns = [
    path("confirmed/", views.order_create, name="order_create"),
    path("checkout/", views.checkout_page, name="checkout_page"),
]
