from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from products.models import product
from .models import cart

# Create your views here.
@login_required(login_url="/login_user/")
def link_cart(request, product_name):
    products = get_object_or_404(product, product_name=product_name)
    try:
        cart.objects.get(cart_product_id=products, cart_auth_id=request.user, check=True)
        return redirect('cart:view_cart')
    except cart.DoesNotExist:
        cart_prod = cart(cart_product_id=products, cart_auth_id=request.user, check=True)
        cart_prod.save()
        return redirect('cart:view_cart')


@login_required(login_url="/login_user/")
def view_cart(request):
    try:
        cart_prod = cart.objects.filter(cart_auth_id=request.user, check=True)
        cart_price = 0.0
        cart_con = 0
        for car in cart_prod:
            p = car.cart_product_id.product_price
            cart_price += p
            cart_con += 1
        cart_quan = True
        return render(request, 'cart/cart.html', {'cart': cart_prod, 'cart_count': cart_quan, 'cart_con': cart_con, 'cart_price': cart_price})
    except cart.DoesNotExist:
        cart_quan = False
        return render(request, 'cart/cart.html', {'cart_count': cart_quan})


@login_required(login_url="/login_user/")
def plus_minus_quntity(request, product_names):
    request.session.modified = True
    products = get_object_or_404(product, product_name=product_names)
    qun = products.product_quantity
    cart_prod = cart.objects.get(cart_auth_id=request.user, cart_product_id=products, check=True)
    if 'plus' in request.POST:
        quantity = request.POST["qun"]
        quantity = int(quantity)
        if quantity == qun:
            print(qun)
            cart_prod.cart_quantity = qun
            cart_prod.save()
        else:
            quantity += 1
            cart_prod.cart_quantity = quantity
            cart_prod.save()
        return redirect('cart:view_cart')
    elif 'minus' in request.POST:
        quantity = request.POST["qun"]
        quantity = int(quantity)
        if quantity == 1:
            cart_prod.cart_quantity = 1
            cart_prod.save()
        else:
            quantity -= 1
            cart_prod.cart_quantity = quantity
            cart_prod.save()
        return redirect('cart:view_cart')


def add_to_cart(request, product_id):
    pass


@login_required(login_url="/login_user/")
def cart_order(request):
    try:
        cart_prod = cart.objects.filter(cart_auth_id=request.user, check=True)
        if not cart_prod:
            return redirect('cart:view_cart')
        else:
            ct = []
            cn = []
            for car in cart_prod:
                ct.append(car.cart_product_id.product_name)
                cn.append(car.cart_quantity)
            request.session['product_lists'] = ct
            request.session['product_qun'] = cn
            print(ct)
            return redirect('cart:fill_address')
    except cart.DoesNotExist:
        return redirect('/')


@login_required(login_url="/login_user/")
def remove_to_cart(request, product_names):
    products = get_object_or_404(product, product_name=product_names)
    try:
        cart_prod = cart.objects.get(cart_auth_id=request.user, cart_product_id=products, check=True)
        cart_prod.check = False
        cart_prod.save()
    except cart.DoesNotExist:
        print('not possible')
    return redirect('cart:view_cart')

