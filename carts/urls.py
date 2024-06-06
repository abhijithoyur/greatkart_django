from django.urls import path
from carts import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('dec_to_cart/<int:product_id>/',views.dec_to_cart,name='dec_to_cart'),
    path('remove_from_cart/<int:product_id>/',views.remove_from_cart,name='remove_from_cart'),
]



