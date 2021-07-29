from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Tobacco, Hookah, Category, LatestProduct, Customer, Cart
from .mixins import CategoryDetailMixin     #импорт миксина!!!


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_up_sidebar()
        products = LatestProduct.object.get_products_for_mainpage('hookah', 'tobacco')
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, 'main/base.html', context)




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


class CartView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_up_sidebar()
        context = {
            'cart': cart,
            'categories': categories
        }
        return render(request, 'main/cart.html', context)



