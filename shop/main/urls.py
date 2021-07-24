
from .views import test_view, ProductDetailView
from django.urls import path




urlpatterns = [
    path('', test_view, name='test'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail')
]

