from django.urls import path
from .api_views import CategoryListAPIView, TobaccoListAPIView


urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('tobaccos/', TobaccoListAPIView.as_view(), name='tobaccos')
]