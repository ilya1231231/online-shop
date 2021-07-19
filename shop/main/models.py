from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.auth import get_user_model    #Хотим использовать пользователя обозначенного в настройках django
User = get_user_model()    #Хотим использовать пользователя обозначенного в настройках django



#1catgory
#2product
#3cartproduct
#4cart
#5order

#6 customer
#7 Specification


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)     #Уникальный Url для отдельной категории

    def __str__(self):    #Возвращаем для представления в Админке
        return self.name


class Product(models.Model):

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


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)     #Внешний ключ на пользователя(кастомера)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')     #Внешний ключ на корзину
    content_type= models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = (GenericForeignKey('content_type', 'object_id'))
    #product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)     #Внешний ключ на продукт
    count = models.PositiveIntegerField(verbose_name='Количество', default=1)    #количество товара
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')


    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.product.title)    #!!!


class Cart(models.Model):

    owner =models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)    #Владелец корзины
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')     #!!!
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

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

class Hookah(Product):
    high = models.CharField(max_length=255, verbose_name='Длина шахты')
    in_material = models.CharField(max_length=255, verbose_name='Материал шахты')
    out_material = models.CharField(max_length=255, verbose_name='Материал накладки')
    pull = models.CharField(max_length=255, verbose_name='Тяга')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)


