from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from .serializers import CategorySerializer, TobaccoSerializer
from ..models import Category, Tobacco


class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TobaccoListAPIView(ListAPIView):

    serializer_class = TobaccoSerializer
    queryset = Tobacco.objects.all()

    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']




