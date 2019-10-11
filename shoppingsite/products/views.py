from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import product_type, product_gallery, product, product_category


# Create your views here.
def index(request):
    request.session.modified = True
    product_type_id = get_object_or_404(product_type, product_type_name='mobiles')
    return render(request, 'products/index.html', {'product_type': product_type_id, 'product_gallery': product_gallery})


def product_view_detail(request, product_types, product_name):
    request.session.modified = True
    product_type_id = get_object_or_404(product_type, product_type_name=product_types)
    product_name = get_object_or_404(product, product_name=product_name)
    pr = product.objects.exclude(product_name=product_name)
    pg = product_name.product_gallery_set.all()
    sender = {'product_type': product_type_id, 'product_name': product_name, 'pg': pg, 'pr': pr}
    return render(request, 'products/product_view.html', sender)


def product_view_listbybrand(request, product_brand_name):
    request.session.modified = True
    try:
        product_type_id = product.objects.filter(product_brand=product_brand_name)
        return render(request, 'products/prodlist.html', {'product_type': product_type_id, 'product_gallery': product_gallery,'name':product_brand_name})
    except product.DoesNotExist:
        return redirect('/')


def product_view_list(request, product_type_names, product_categorys):
    request.session.modified = True
    product_cate = get_object_or_404(product_category, product_category_name=product_categorys)
    product_type_id = get_object_or_404(product_type, product_type_name=product_type_names, product_category_id=product_cate)
    return render(request, 'products/fil&search.html', {'product_type': product_type_id, 'product_gallery': product_gallery})


def search(request):
    request.session.modified = True
    prodt = product.objects.all()
    query = request.GET.get("q")
    if query:
        prod = prodt.distinct()\
                    .filter(Q(product_name__icontains=query) | Q(product_brand__icontains=query))
        return render(request, 'products/prodlist.html', {'product_type': prod, 'product_gallery': product_gallery})
    else:
        return render(request, 'products/prodlist.html', {'product_type': prodt})


