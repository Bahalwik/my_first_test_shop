from django.shortcuts import render
from .models import *
from django.http import JsonResponse


def home(request):
    products_images = ProductImg.objects.filter(is_active=True, is_main=True, product__is_active=True)
    products_images_phones = products_images.filter(product__category_id=1)
    products_images_laptops = products_images.filter(product__category_id=3)
    products_images_pads = products_images.filter(product__category_id=2)
    return render(request, 'advertisements_app/home.html', locals())


def product(request, product_id):

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    print(request.session.session_key)

    product = Product.objects.get(id=product_id)
    return render(request, 'advertisements_app/product.html', locals())


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    new_product = ProductInBasket.objects.create(session_key=session_key, product_id=product_id, nmb=nmb)
    products_total_nmb = ProductInBasket.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["products_total_nmb"] = products_total_nmb
    return JsonResponse(return_dict)
