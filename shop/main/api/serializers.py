from rest_framework import serializers
from ..models import Category, Tobacco


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug'
        ]


class BaseProductSerializer:
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)   #Изпользуется в API вместо ForeignKey,передается кверисет в котором осуществляется поиск
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    product_image = serializers.ImageField(required=True)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=9, decimal_places=2, required=True)


class TobaccoSerializer(BaseProductSerializer, serializers.ModelSerializer):
    taste = serializers.CharField(required=True)
    strength = serializers.CharField(required=True)
    structure = serializers.CharField(required=True)
    size = serializers.CharField(required=True)

    class Meta:
        model = Tobacco
        fields = '__all__'

