from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^product/(?P<product_id>\w+)/$', views.product, name='product'),
    path('basket_adding', views.basket_adding, name='basket_adding'),
    # path('contacts', views.contacts, name='contacts'),
    # path('about', views.about, name='about')
]
