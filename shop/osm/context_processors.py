from .models import product_category


def add_variable_to_context(request):
    product = product_category.objects.all()
    no = 10
    return {
        'product_category': product,
        'no': no
    }
