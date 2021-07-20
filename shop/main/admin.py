from django.contrib import admin
from .models import *
from django import forms




'''Функция выбора категории,характерной для продукта <Tobacco>'''
class TobaccoCategoryChoiceField(forms.ModelChoiceField):

    pass


class TobaccoAdmin(admin.ModelAdmin):

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
