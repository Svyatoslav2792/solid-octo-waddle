# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from newsite1app1.views import (
        base_view,
        category_view,
        product_view,
        cart_view,
        add_to_cart_view,
        remove_from_cart_view,
        change_item_qty,
        checkout_view,
        order_create_view,
        make_order_view,
        account_view,
        registration_view,
        login_view
        )
        

urlpatterns = [
    path('category/<str:category_slug>', category_view, name='category_detail'),
    path('product/<str:product_slug>', product_view, name='product_detail'),   
    path('add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart_view, name='remove_from_cart'),
    path('change_item_qty/', change_item_qty, name='change_item_qty'),
    path('cart/', cart_view, name='cart'),
    path('checkout_view/', checkout_view, name='checkout'),
    path('order_create_view/', order_create_view, name='order_create'),
    path('make_order_view/', make_order_view, name='make_order_view'),
    path('account/', account_view, name= 'account'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='base'), name='logout'),
    path('', base_view, name='base'),
    
]
