from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from .serializers import CategorySerializer, TobaccoSerializer, HookahSerializer
from ..models import Category, Tobacco, Hookah


class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TobaccoListAPIView(ListAPIView):

    serializer_class = TobaccoSerializer
    queryset = Tobacco.objects.all()

    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class TobaccoDetailAPIView(RetrieveAPIView):    #Вместо DetailView

    serializer_class = TobaccoSerializer
    queryset = Tobacco.objects.all()


class HookahListAPIView(ListAPIView):

    serializer_class = HookahSerializer
    queryset = Hookah.objects.all()


class HookahDetailAPIView(RetrieveAPIView):

    serializer_class = HookahSerializer
    queryset = Hookah.objects.all()





