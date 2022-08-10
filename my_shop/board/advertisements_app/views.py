from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from .forms import *
from django.contrib.auth.models import User


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

    new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                 defaults={"nmb": nmb})
    if not created:
        new_product.nmb += int(nmb)
        new_product.save(force_update=True)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    form = CheckoutForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            data = request.POST
            phone = data["phone"]
            name = data["name"]
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)

            for name, value in data.items():

                if name.startswith("product_in_basket"):
                    product_in_basket_id = name.split("product_in_basket")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)

                    product_in_basket.nmb = value
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price, order=order)


    return render(request, 'advertisements_app/checkout.html', locals())
