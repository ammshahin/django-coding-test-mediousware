from django.db.models import fields
from rest_framework import serializers
from .models import Product, ProductVariant, ProductVariantPrice, ProductImage


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        exclude = [
            "id",
        ]


class ProductSerializer(serializers.ModelSerializer):

    # productvariantprice = ProductVariantPriceSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'
        lookup_field = 'product'


class ProductVariantPriceSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductVariantPrice
        exclude = [
            "id",
        ]

    def create(self, validated_data):
        product = validated_data.pop("product")
        product = Product.create(
            ProductSerializer(), validated_data=product
        )

        productprice, created = ProductVariantPrice.objects.update_or_create(
            product=product,

            price=validated_data.pop("price"),
            stock=validated_data.pop("stock"),

        )
        return productprice