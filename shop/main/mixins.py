from django.views.generic.detail import SingleObjectMixin
from .models import Category

class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):       #Получаем данные категории
        context = super().get_context_data(**kwargs)    #результат работы метода
        context['categories'] = Category.objects.get_categories_for_up_sidebar()
        return context

