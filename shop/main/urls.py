
from .views import test_view, ProductDetailView, CategoryDetailView
from django.urls import path




urlpatterns = [
    path('', test_view, name='test'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
]

'''ct_model и slug из функции get_absolute_url, name -это viewname, которое мы передавали в функцию GAU моделей
    Tobacco и Hookah'''