from django.views.generic.detail import SingleObjectMixin
from .models import Category, Cart, Customer
from django.views.generic import View

class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):       #Получаем данные категории
        context = super().get_context_data(**kwargs)    #результат работы метода
        context['categories'] = Category.objects.get_categories_for_up_sidebar()
        return context


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            '''Ищем корзину,которая относится к этому пользователю и которая не находится в заказе'''
            customer=Customer.objects.filter(user=request.user).first()
            cart= Cart.objects.filter(owner=customer, in_order=False).first()
            '''Все остальные поля сделали нулевыми'''
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            '''Если найдена-возвращаем,если нет-создаем'''
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart

        return super().dispatch(request, *args, **kwargs)


