from django.shortcuts import render

from reward.models import Product


def index(request):
    # TEMPLATE 설정 app/template 추

    products = Product.objects.all()

    print('메인페이지')

    context = {
        'products': products
    }

    return render(request, 'production/product-list.html', context)
