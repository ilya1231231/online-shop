
from .views import test_view
from django.urls import path


urlpatterns = [
    path('', test_view, name='test')
]

