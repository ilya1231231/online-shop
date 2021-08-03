from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from .models import Tobacco, Hookah, Category, LatestProduct, Customer, Cart, CartProduct
from .mixins import CategoryDetailMixin, CartMixin    #импорт миксина
from django.contrib import messages


class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        '''Поля реализованы в Миксине'''
        # customer = Customer.objects.get(user=request.user)
        # cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_up_sidebar()
        products = LatestProduct.object.get_products_for_mainpage('hookah', 'tobacco')
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart
        }
        return render(request, 'main/base.html', context)




class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
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


    '''Добавляем информацию о конкретной модели в класс(строковое представление)'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'main/category_detail.html'
    slug_url_kwarg = 'slug'


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')     #берем нужные значения
        '''Поля реализованы в Миксине'''
        # customer = Customer.objects.get(user= request.user)     #берем покупателя
        #cart = Cart.objects.get(owner = customer, in_order = False)     #берем корзину
        content_type = ContentType.objects.get(model=ct_model)      #берем модель нашего товара
        product = content_type.model_class().objects.get(slug=product_slug)     #получаем продукт у объекта Content_type через родительский класс,обращаеся через менеджер находя продукт по слагу
        ''' создаем новый cart_product объект с набором аргументов'''
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        if created:
            self.cart.products.add(cart_product)
        self.cart.save()    #информация обновляется при добавлении товара в корзину
        messages.add_message(request, messages.INFO, 'Товар успешно добавлен в корзину')

        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')

        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Товар успешно удален из корзины')
        return HttpResponseRedirect('/cart/')

class ChangeCountView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        '''присваиваем значение, которое приходит из тела запроса'''
        qty = int(request.POST.get('qty'))
        cart_product.count = qty
        cart_product.save()
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Количество товара успешно изменено')
        #print(request.POST)
        return HttpResponseRedirect('/cart/')





class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        '''Поля реализованы в Миксине'''
        # customer = Customer.objects.get(user=request.user)
        # cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_up_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'main/cart.html', context)



