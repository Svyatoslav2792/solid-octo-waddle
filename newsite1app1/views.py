from django.shortcuts import render
from newsite1app1.models import Category, Product, CartItem, Cart, Order
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from decimal import Decimal
from newsite1app1.forms import OrderForm, RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate
import smtplib


def base_view(request):
    try:
        cart_id= request.session['cart_id']
        cart=Cart.objects.get(id=cart_id)
        request.session['total']= cart.items.count()
    except:
            cart=Cart()
            cart.save()
            cart_id=cart.id
            request.session['cart_id']=cart_id
            cart=Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    products = Product.objects.filter(availible=True)
    context = {
            'categories': categories,
            'products': products,
            'cart': cart
            }
    return render(request, 'base.html', context)

def product_view(request, product_slug):
    try:
        cart_id= request.session['cart_id']
        cart=Cart.objects.get(id=cart_id)
        request.session['total']= cart.items.count()
    except:
            cart=Cart()
            cart.save()
            cart_id=cart.id
            request.session['cart_id']=cart_id
            cart=Cart.objects.get(id=cart_id)
    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all()
    context = {
            'product': product,
            'categories': categories,
            'cart': cart
            }
    return render(request, 'product.html', context)

def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products_of_category = category.product_set.all()
    categories = Category.objects.all()
    context = {
            'category':category,
            'products_of_category':products_of_category,
            'categories': categories
            }
    return render(request, 'category.html', context)
# Create your views here.

def cart_view(request):
    categories = Category.objects.all()
    try:
        cart_id= request.session['cart_id']
        cart=Cart.objects.get(id=cart_id)
        request.session['total']= cart.items.count()
    except:
            cart=Cart()
            cart.save()
            cart_id=cart.id
            request.session['cart_id']=cart_id
            cart=Cart.objects.get(id=cart_id)
    context ={
            'cart':cart,
            'categories': categories,
            }
    return render(request, 'cart.html', context)

def add_to_cart_view(request):
    try:
        cart_id= request.session['cart_id']
        cart=Cart.objects.get(id=cart_id)
        request.session['total']= cart.items.count()
    except:
            cart=Cart()
            cart.save()
            cart_id=cart.id
            request.session['cart_id']=cart_id
            cart=Cart.objects.get(id=cart_id)
    product_slug=request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    new_cart_total=0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total':cart.items.count(),'cart_total_price': cart.cart_total})
        
def remove_from_cart_view(request):
    try:
        cart_id= request.session['cart_id']
        cart=Cart.objects.get(id=cart_id)
        request.session['total']= cart.items.count()
    except:
            cart=Cart()
            cart.save()
            cart_id=cart.id
            request.session['cart_id']=cart_id
            cart=Cart.objects.get(id = cart_id)
    product_slug=request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product_slug)
    new_cart_total=0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total':cart.items.count(),'cart_total_price': cart.cart_total})
    
def change_item_qty(request):
        try:
            cart_id= request.session['cart_id']
            cart=Cart.objects.get(id=cart_id)
            request.session['total']= cart.items.count()
        except:
            cart=Cart()
            cart.save()
            cart_id=cart.id
            request.session['cart_id']=cart_id
            cart=Cart.objects.get(id = cart_id)
        qty=request.GET.get('qty')
        item_id=request.GET.get('item_id')
        cart.cart_change_qty(qty, item_id)
        cart_item=CartItem.objects.get(id=int(item_id))
        return JsonResponse({'cart_total': cart.items.count(),
                             'item_total': cart_item.item_total,
                             'cart_total_price': cart.cart_total})
    
def checkout_view(request):
     categories = Category.objects.all()
     try:
            cart_id= request.session['cart_id']
            cart=Cart.objects.get(id=cart_id)
            request.session['total']= cart.items.count()
     except:
         cart=Cart()
         cart.save()
         cart_id=cart.id
         request.session['cart_id']=cart_id
         cart=Cart.objects.get(id = cart_id)
     context= {
                'cart':cart,
                'categories': categories,
                }
     return render(request, 'checkout.html', context)

def order_create_view(request):
    try:
            cart_id= request.session['cart_id']
            cart=Cart.objects.get(id=cart_id)
            request.session['total']= cart.items.count()
    except:
         cart=Cart()
         cart.save()
         cart_id=cart.id
         request.session['cart_id']=cart_id
         cart=Cart.objects.get(id = cart_id)
    form=OrderForm(request.POST or None)
    categories = Category.objects.all()
    context = {
            'form': form,
            'categories': categories,
            }    
    return render(request, 'order.html', context)

def make_order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        new_order = Order()
        new_order.user = request.user
        new_order.save()
        new_order.items.add(cart)
        new_order.first_name = name
        new_order.last_name = last_name
        new_order.phone = phone
        new_order.address = address
        new_order.buying_type = buying_type
        new_order.comments = comments
        new_order.total = cart.cart_total
        new_order.save()
        request.session['total'] = cart.items.count()
        del request.session['cart_id']
        del request.session['total']
        return render(request, 'thank_you.html') 
    return render(request, 'order.html', {'categories': categories})

def account_view(request):
    order=Order.objects.filter(user=request.user).order_by('-id')
    categories = Category.objects.all()
    context={
            'order':order,
            'categories':categories
            }
    return render(request, 'account.html', context)

def registration_view(request):
    form = RegistrationForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
       new_user=form.save(commit=False)
       first_name=form.cleaned_data['first_name']
       last_name=form.cleaned_data['last_name']
       username=form.cleaned_data['username']
       password=form.cleaned_data['password']
       email=form.cleaned_data['email']

       new_user.username=username
       new_user.set_password(password)
       new_user.email=email
       new_user.first_name=first_name
       new_user.last_name=last_name
       new_user.save()
       login_user=authenticate(username=username,password=password)
       if login_user:
            login(request, login_user)
            smtpObj = smtplib.SMTP_SSL('smtp.mail.ru', 465)
            smtpObj.login('mamkin.raketchik@mail.ru', 'fastfighter92')
            smtpObj.sendmail("mamkin.raketchik@mail.ru", "fastfighter92@gmail.com", "New user added in database "+new_user.email)
            smtpObj.quit()
            return HttpResponseRedirect(reverse('base'))
    context = {
            'form': form,
            'categories':categories
            }
    return render(request,'registration.html', context)

def login_view(request):
    form=LoginForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        login_user=authenticate(username=username,password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context={
            'form':form,
            'categories':categories
            }
    return render(request, 'login.html', context)
