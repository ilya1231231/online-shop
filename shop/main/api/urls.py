from django.urls import path
from .api_views import (CategoryListAPIView,
                        TobaccoListAPIView,
                        HookahListAPIView,
                        TobaccoDetailAPIView,
                        HookahDetailAPIView
)


urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories_list'),
    path('tobaccos/', TobaccoListAPIView.as_view(), name='tobaccos_list'),
    path('hookahs/', HookahListAPIView.as_view(), name='hookahs_list'),
    path('tobaccos/<str:pk>/', TobaccoDetailAPIView.as_view(), name='tobacco_detail'),
    path('hookahs/<str:pk>/', HookahDetailAPIView.as_view(), name='hookah_detail')
]