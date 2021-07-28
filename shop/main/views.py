from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Tobacco, Hookah, Category
from .mixins import CategoryDetailMixin     #импорт миксина!!!


class BaseView(CategoryDetailMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_up_sidebar()
        return render(request, 'main/base.html', {'categories': categories})




class ProductDetailView(CategoryDetailMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'tobacco': Tobacco,
        'hookah': Hookah
    }

    '''Забираем модель из запроса,чтобы получить определенную модель '''
    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]    #Имя модели передается через словарь для формирования URL
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    # model = Model
    # queryset = Model.objects.all()
    context_object_name = 'product'     #просто контекстное имя
    template_name = 'main/product_detail.html'    #обязательно путь до папки,если шаблон не находится в templates
    slug_url_kwarg = 'slug'    #Для использования слага


class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'main/category_detail.html'
    slug_url_kwarg = 'slug'

