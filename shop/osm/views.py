from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from datetime import datetime, timedelta, date
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserForm, MobileForm, AddressForm
from .models import product_type, product_gallery, product, order_info, order, address_info, product_category, cart
from django.contrib.auth.decorators import login_required


def login_user(request):
    request.session.modified = True
    if not request.user.is_authenticated:
        next_url = request.GET.get('next')
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if next_url:
                        print('next_url')
                        return redirect(next_url)
                    else:
                        return redirect('/')
                else:
                    error = {'error_message': 'Your account has been disabled'}
                    return render(request, 'osm/login.html', error)
            else:
                error = {'error_message': 'Invaild Username or Password'}
                return render(request, 'osm/login.html', error)
        return render(request, 'osm/login.html')
    else:
        return redirect('/')


def logout_user(request):
    request.session.modified = True
    logout(request)
    return redirect('/')


def register(request):
    request.session.modified = True
    if not request.user.is_authenticated:
        next_url = request.POST.get('next')
        u_form = UserForm(request.POST or None)
        m_form = MobileForm(request.POST or None)
        if u_form.is_valid() and m_form.is_valid():
            user_f = u_form.save(commit=False)
            mobile = m_form.save(commit=False)
            username = u_form.cleaned_data['username']
            password = u_form.cleaned_data['password']
            user_f.set_password(password)
            user_f.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    mobile.m_id = request.user
                    print(request.user)
                    mobile.save()
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('/')
        context = {'u_form': u_form, 'm_form': m_form}
        return render(request, 'osm/reg.html', context)
    else:
        return redirect('/')


def index(request):
    request.session.modified = True
    print(date.today())
    product_type_id = get_object_or_404(product_type, product_type_name='mobiles')
    return render(request, 'osm/index.html', {'product_type': product_type_id, 'product_gallery': product_gallery})


def search_found(request):
    request.session.modified = True
    prodt = product.objects.all()
    query = request.GET.get("q")
    if query:
        prod = prodt.distinct()\
                    .filter(Q(product_name__icontains=query) | Q(product_brand__icontains=query))
        return render(request, 'osm/prodlist.html', {'product_type': prod, 'product_gallery': product_gallery})
    else:
        return render(request, 'osm/prodlist.html', {'product_type': prodt})


@login_required(login_url="/login_user/")
def link_cart(request, product_name):
    products = get_object_or_404(product, product_name=product_name)
    try:
        cart.objects.get(cart_product_id=products, cart_auth_id=request.user, check=True)
        return redirect('osm:view_cart')
    except cart.DoesNotExist:
        cart_prod = cart(cart_product_id=products, cart_auth_id=request.user, check=True)
        cart_prod.save()
        return redirect('osm:view_cart')


@login_required(login_url="/login_user/")
def view_cart(request):
    request.session.modified = True
    try:
        cart_prod = cart.objects.filter(cart_auth_id=request.user, check=True)
        cart_price = 0.0
        cart_con = 0
        for car in cart_prod:
            p = car.cart_product_id.product_price
            cart_price += p
            cart_con += 1
        cart_quan = True
        return render(request, 'osm/cart.html', {'cart': cart_prod, 'cart_count': cart_quan, 'cart_con': cart_con, 'cart_price': cart_price})
    except cart.DoesNotExist:
        cart_quan = False
        return render(request, 'osm/cart.html', {'cart_count': cart_quan})


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
        return redirect('osm:view_cart')
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
        return redirect('osm:view_cart')


def add_to_cart(request, product_id):
    pass


@login_required(login_url="/login_user/")
def cart_order(request):
    try:
        cart_prod = cart.objects.filter(cart_auth_id=request.user, check=True)
        if not cart_prod:
            return redirect('osm:view_cart')
        else:
            ct = []
            cn = []
            for car in cart_prod:
                ct.append(car.cart_product_id.product_name)
                cn.append(car.cart_quantity)
            request.session['product_lists'] = ct
            request.session['product_qun'] = cn
            print(ct)
            return redirect('osm:fill_address')
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
    return redirect('osm:view_cart')


def product_detail(request, product_types, product_name):
    request.session.modified = True
    product_type_id = get_object_or_404(product_type, product_type_name=product_types)
    product_name = get_object_or_404(product, product_name=product_name)
    pr = product.objects.exclude(product_name=product_name)
    pg = product_name.product_gallery_set.all()
    sender = {'product_type': product_type_id, 'product_name': product_name, 'pg': pg, 'pr': pr}
    return render(request, 'osm/product_view.html', sender)


def product_list_brand(request, product_brand_name):
    request.session.modified = True
    try:
        product_type_id = product.objects.filter(product_brand=product_brand_name)
        return render(request, 'osm/prodlist.html', {'product_type': product_type_id, 'product_gallery': product_gallery})
    except product.DoesNotExist:
        return redirect('/')


def product_list(request, product_type_names, product_categorys):
    request.session.modified = True
    product_cate = get_object_or_404(product_category, product_category_name=product_categorys)
    product_type_id = get_object_or_404(product_type, product_type_name=product_type_names, product_category_id=product_cate)
    return render(request, 'osm/fil&search.html', {'product_type': product_type_id, 'product_gallery': product_gallery})


@login_required(login_url="/login_user/")
def order_buy(request, product_names):
    product_na = get_object_or_404(product, product_name=product_names)
    if product_na.product_quantity == 0:
        return redirect('/')
    else:
        list = []
        list.append(product_names)
        request.session['product_lists'] = list
        request.session['product_qun'] = [1]
        print(list)
    return redirect('osm:fill_address')


@login_required(login_url="/login_user/")
def fill_address(request):
    if 'product_lists' not in request.session:
        return redirect('/')
    else:
        form = AddressForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile_no']
            pincode = form.cleaned_data['pincode']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            form.save(commit=False)
            form_data = [name, mobile, pincode, address, city, state]
            request.session['form'] = form_data
            return redirect('osm:payment_method')
        else:
            context = {'add_form': form}
            return render(request, 'osm/address.html', context)


@login_required(login_url="/login_user/")
def payment_method(request):
    if 'form' not in request.session:
        return redirect('/')
    else:
        if 'product_lists' not in request.session:
            return redirect('/')
        else:
            if request.method == "POST":
                payment = request.POST['pay']
                request.session['payment'] = payment
                if payment == 'cod':
                    request.session['payment'] = "cod"
                    return redirect('osm:order_summary')
                else:
                    return render(request, 'osm/payment_method.html')
            else:
                return render(request, 'osm/payment_method.html')


@login_required(login_url="/login_user/")
def order_summary(request):
    if 'product_lists' not in request.session:
        return redirect('/')
    else:
        products = request.session['product_lists']
        pr_qun = request.session['product_qun']
        print(products)
        print(pr_qun)
        pr_qun = list(pr_qun)
        form = request.session['form']
        add_form = address_info(name=form[0], mobile_no=form[1], pincode=form[2], address=form[3], city=form[4], state=form[5])
        pay = request.session['payment']
        id = []
        for pr, quantitys in zip(products, pr_qun):
            prod = product.objects.get(product_name=pr)
            quan = quantitys
            prods = prod.product_quantity
            prods -= 1
            prod.product_quantity = prods
            ord_inf = order_info()
            ord_inf.order_date = datetime.today()
            ord_inf.order_payment_method = pay
            ord_inf.order_quantity = quan
            ord_inf.order_total_payment = prod.product_price * quan
            today = datetime.today()
            nows = today + timedelta(days=10)
            ord_inf.order_delivery_date = nows
            ord_inf.save()
            prod.save()
            add_form.save()
            ord = order(order_product_id=prod, order_auth_id=request.user, order_address_id=add_form, order_info_id=ord_inf)
            ord.save()
            global id
            id.append(ord.pk)
            print('ids-', id)
            try:
                cart_prod = cart.objects.get(cart_auth_id=request.user, check=True, cart_product_id=prod)
                cart_prod.check = False
                cart_prod.save()
            except cart.DoesNotExist:
                pass
        request.session.modified = True
        request.session['order'] = id
        return redirect('osm:order-report')


@login_required(login_url="/login_user/")
def report(request):
    if 'order' not in request.session:
        return redirect('/')
    else:
        v = request.session['order']
        plus = 0
        prices = 0.0
        for i in v:
            price = order.objects.get(pk=i)
            plus += 1
            p = price.order_info_id.order_total_payment
            prices += p
        orders = order.objects.all()
        return render(request, 'osm/order-summary.html', {'orders': orders, 'total': prices, 'count': plus})


def total_report(request):
    orders = order.objects.filter(order_auth_id=request.user)
    return render(request, 'osm/total-order-summary.html', {'orders': orders})
