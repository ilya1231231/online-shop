from django.contrib import admin
from .models import *
from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.safestring import mark_safe      #позволяет добавить в строку python Тэг html

from PIL import Image


class TobaccoAdminForm(ModelForm):

    '''Текст помощник'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_image'].help_text = mark_safe(
            '<span style="color:red;">При загрузке изображения с разрешением больше {} x {} ,оно будет обрезано  </span>'.format(
                *Product.MAX_RESOLUTION
            )
        )
    '''Функция для проверки разрешения изображения'''
    def clean_product_image(self):
        image = self.cleaned_data['product_image']
        img = Image.open(image)
        min_width, min_height = Product.MIN_RESOLUTION
        max_width, max_height = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:     #ограничение загрузки изображения размером больше 3 МБ
            raise ValidationError('Размер изображения слишком большой')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Загруженное изображение меньше минимального')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Загруженное изображение больше минимального')
        return image



class HookahAdminForm(ModelForm):

    '''Текст помощник'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_image'].help_text = mark_safe(
            '<span style="color:red;">При загрузке изображения с разрешением больше {} x {} ,оно будет обрезано  </span>'.format(
                *Product.MAX_RESOLUTION
            )
        )
    '''Функция для проверки разрешения изображения'''
    def clean_product_image(self):
        image = self.cleaned_data['product_image']
        img = Image.open(image)
        min_width, min_height = Product.MIN_RESOLUTION
        max_width, max_height = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:     #ограничение загрузки изображения размером больше 3 МБ
            raise ValidationError('Размер изображения слишком большой')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Загруженное изображение меньше минимального')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Загруженное изображение больше минимального')
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
