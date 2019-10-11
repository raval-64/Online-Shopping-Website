from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import address_info, order, order_info
from datetime import datetime, timedelta, date
from products.models import product
from .forms import AddressForm, ProcessForm
from cart.models import cart

# Create your views here.
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
    return redirect('order:fill_process')


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
            return redirect('order:payment_method')
        else:
            context = {'add_form': form}
            return render(request, 'order/address.html', context)

@login_required(login_url="/login_user/")
def fill_process(request):
    if 'product_lists' not in request.session:
        return redirect('/')
    else:
        form = ProcessForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile_no']
            pincode = form.cleaned_data['pincode']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pay = form.cleaned_data['pay']
            form.save(commit=False)
            form_data = [name, mobile, pincode, address, city, state, pay]
            request.session['form'] = form_data
            return redirect('order:order_summary')
        else:
            context = {'form': ProcessForm}
            return render(request, 'order/process.html',context)

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
                    return redirect('order:order_summary')
                else:
                    return render(request, 'order/payment_method.html')
            else:
                return render(request, 'order/payment_method.html')


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
        pay = form[6]
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
            id
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
        return redirect('order:order-report')


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
        return render(request, 'order/order-summary.html', {'orders': orders, 'total': prices, 'count': plus})

@login_required(login_url="/login_user/")
def total_report(request):
    orders = order.objects.filter(order_auth_id=request.user)
    return render(request, 'order/total-order-summary.html', {'orders': orders})
