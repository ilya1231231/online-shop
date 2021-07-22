from django.contrib import admin
from .models import *
from django import forms
from django.forms import ModelForm, ValidationError

from PIL import Image


class TobaccoAdminForm(ModelForm):

    MIN_RESOLUTION = (4000, 4000)
    '''Текст помощник'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_image'].help_text = 'Загружайте изображение с минимальным разрешением {} x {}'.format(
            *self.MIN_RESOLUTION
        )
    '''Функция для проверки разрешения изображения'''
    def clean_product_image(self):
        image = self.cleaned_data['product_image']
        img = Image.open(image)
        min_width, min_height = self.MIN_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Загруженное изображение меньше минимального')
        return image



'''Функция выбора категории,характерной для продукта <Tobacco>'''
class TobaccoCategoryChoiceField(forms.ModelChoiceField):

    pass


class TobaccoAdmin(admin.ModelAdmin):

    form = TobaccoAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return TobaccoCategoryChoiceField(Category.objects.filter(slug='tobaccos'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



'''Функция выбора категории,характерной для продукта <Hookah>'''

class HookahCategoryChoiceField(forms.ModelChoiceField):

    pass


class HookahAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return TobaccoCategoryChoiceField(Category.objects.filter(slug='hookahs'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Tobacco, TobaccoAdmin)
admin.site.register(Hookah, HookahAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
