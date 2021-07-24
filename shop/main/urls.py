
from .views import test_view, ProductDetailView
from django.urls import path




urlpatterns = [
    path('', test_view, name='test'),
    '''ct_model и slug из функции get_absolute_url, name -это viewname, которое мы передавали в функцию GAU моделей
    Tobacco и Hookah'''
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail')
]

