from django.conf import settings
from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("__all__")


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ('image_url',)

    def get_image_url(self, obj):
        return obj.image_url


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('created_by',)

    def get_images(self, obj):
        images_queryset = obj.product_images.all()
        request = self.context.get('request')
        if request:
            media_url = request.build_absolute_uri('/media/')
            return [media_url+str(img.image_url) for img in images_queryset]
        else:
            return [str(img.image_url) for img in images_queryset]
