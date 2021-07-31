import sys
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import get_user_model    #Хотим использовать пользователя обозначенного в настройках django
from django.urls import reverse

def get_models_for_count(*model_names):    #!!!!!!!!!!!
    return [models.Count(model_name) for model_name in model_names]

'''Менеджер для поседующего отображения категорий и товаров, имеющихся в ней'''
class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Табаки': 'tobacco__count',
        'Кальяны': 'hookah__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_up_sidebar(self):    #!!!!!!!!!!!!!!!!
        models = get_models_for_count('tobacco', 'hookah')
        qs = list(self.get_queryset().annotate(*models))   #Искольная функция
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data



User = get_user_model()    #Хотим использовать пользователя обозначенного в настройках django

'''Делаем url для каждого отдельного продукта'''
def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name       #передаем имя модели через атрибут 'meta' в ct_model
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})    #передаем в кварги имя и слаг объекта




class MinResolutionErrorException(Exception):     #кастомная ошибка для минимального разрешения
    pass


class MaxResolutionErrorException(Exception):     #кастомная ошибка для максимального разрешения
    pass



class LatestProductManager:

    @staticmethod
    def get_products_for_mainpage(*args, **kwargs):     #функция получить все товары для отображения на главной странице
        for_respect = kwargs.get('for_respect')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)     #Фильтруем модели в аргументах
        for ct_model in ct_models:                                 #Итерируемся по моделям
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]     #Берем все объекты из родительскиго класса
            products.extend(model_products)
            '''for_respect принимает параметр той категории,которую нужно отобразить первой '''
        if for_respect:
            ct_model = ContentType.objects.filter(model=for_respect)
            if ct_model.exists():
                if for_respect in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(for_respect), reverse=True     #!!!!!!!
                    )
        return products



class LatestProduct:

    object = LatestProductManager()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)     #Уникальный Url для отдельной категории
    objects = CategoryManager()

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):    #Возвращаем для представления в Админке
        return self.name


class Product(models.Model):
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (1200, 1200)
    MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)     #показывает,что товар пренадлежит категории
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    slug = models.SlugField(unique=True)
    product_image = models.ImageField(verbose_name='Изображение товара')
    description = models.TextField(verbose_name='Описание', null=True)    #null указывает,что поле может быть пустым
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')     #2 аргумента, из скольки цифр состоит число большее и меньшее

    def __str__(self):    #Возвращаем для представления в Админке
        return self.title


    def save(self, *args, **kwargs):

        '''Проверяем изображение при сохранении'''
        image = self.product_image
        img = Image.open(image)
        min_width, min_height = self.MIN_RESOLUTION
        max_width, max_height = self.MAX_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException('Загруженное изображение меньше минимального')
        if img.height > max_height or img.width > max_width:
            raise MaxResolutionErrorException('Загруженное изображение больше минимального')

        '''При сохранении принудительное изменение разрешения изображения, применяемого на сайте'''
        # image = self.product_image
        # img = Image.open(image)
        # new_img = img.convert('RGB')     #!!!!!!!!!!!!
        # resized_new_img = new_img.resize((200, 200), Image.ANTIALIAS)
        # filestream = BytesIO()
        # resized_new_img.save(filestream, 'JPEG', quality=90)
        # filestream.seek(0)
        # name = '{}.{}'.format(*self.product_image.name.split('.'))     #допускаются файлы с определенным именем
        # self.product_image = InMemoryUploadedFile(
        #     filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
        # )

        super().save(*args, **kwargs)         #!!!!!!!!!!!!!!


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)     #Внешний ключ на пользователя(кастомера)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')     #Внешний ключ на корзину
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = (GenericForeignKey('content_type', 'object_id'))
    #product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)     #Внешний ключ на продукт
    count = models.PositiveIntegerField(verbose_name='Количество', default=1)    #количество товара
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')


    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.content_object.title)    #!!!

    def save(self,*args, **kwargs):     #Для решения проблемы,при изменении атрибутов модели
        self.total_price = self.count *self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner =models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)    #Владелец корзины
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')     #!!!
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)     #!!!


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=250, verbose_name='Адрес пользователя')

    def __str__(self):
        return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)     #!!!



class Tobacco(Product):
    taste = models.CharField(max_length=255, verbose_name='Вкус табака')
    strength = models.CharField(max_length=255, verbose_name='Крепость табака')
    structure = models.CharField(max_length=255, verbose_name='Нарезка табака')
    size = models.CharField(max_length=255, verbose_name='Возможные граммовки')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')    #передает результат функции и передаем viewname из той функции

class Hookah(Product):
    high = models.CharField(max_length=255, verbose_name='Длина шахты')
    in_material = models.CharField(max_length=255, verbose_name='Материал шахты')
    out_material = models.CharField(max_length=255, verbose_name='Материал накладки')
    pull = models.CharField(max_length=255, verbose_name='Тяга')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')






