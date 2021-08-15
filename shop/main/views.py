from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from .models import Tobacco, Hookah, Category, LatestProduct, CartProduct, Customer
from .mixins import CategoryDetailMixin, CartMixin    #импорт миксина
from django.contrib import messages
from .forms import OrderForm
from .utils import recount_cart


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
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'main/category_detail.html'
    slug_url_kwarg = 'slug'

    '''Добавляем информацию о конкретной модели в класс(строковое представление)'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


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
        recount_cart(self.cart)    #информация обновляется при добавлении товара в корзину
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
        recount_cart(self.cart)
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
        recount_cart(self.cart)
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


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        '''Поля реализованы в Миксине'''
        # customer = Customer.objects.get(user=request.user)
        # cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_up_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'main/checkout.html', context)

class MakeOrderView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            '''Созданный инстанс,который нужно предзаполнить чтобы сохранить'''
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            self.cart.in_order = True
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            recount_cart(self.cart)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ, менеджер с вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')




