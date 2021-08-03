
from .views import (BaseView,
                    ProductDetailView,
                    CategoryDetailView,
                    CartView,
                    AddToCartView,
                    DeleteFromCartView,
                    ChangeCountView
                    )
from django.urls import path


urlpatterns = [
    path('', BaseView.as_view(), name='test'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete_from_cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change_count/<str:ct_model>/<str:slug>/', ChangeCountView.as_view(), name='change_count')
]

'''ct_model и slug из функции get_absolute_url, name -это viewname, которое мы передавали в функцию GAU моделей
    Tobacco и Hookah'''