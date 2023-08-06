from django.http import HttpRequest
from rest_framework import serializers

from product_module.models import *


class ProductSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True, required=False)
    image = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True, required=False)
    votes_avg = serializers.IntegerField(source="vote_avg", read_only=True)
    # category = serializers.SlugRelatedField(many=False, read_only=False, slug_field="title",
    #                                         queryset=ProductCategory.objects.all())
    # brand = serializers.CharField(source="brand.title", read_only=True)
    # category = serializers.CharField(source="category.title", read_only=True)
    gallery = serializers.SerializerMethodField(method_name="get_galley")

    def to_representation(self, instance: Product):
        rep = super(ProductSerializer, self).to_representation(instance)
        request: HttpRequest = self.context.get("request")
        if request.parser_context.get("kwargs").get("pk"):
            details = {}
            for attribute in instance.product_attributes.prefetch_related("product_detail").all():
                details.update({attribute.product_detail.key: attribute.value})
            rep["details"] = details
        else:
            rep.pop("description")
            # pass
        return rep

    def get_galley(self, obj):
        request = self.context.get('request')
        gallery = ProductGallery.objects.filter(product_id=obj.id)
        images = []
        for image in gallery:
            image_url = request.build_absolute_uri(image.image.url)
            images.append(image_url)
        return images

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["votes_avg"]


class ProductCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(method_name="get_children")

    class Meta:
        model = ProductCategory
        fields = ["id", "title", "slug", "is_active", "is_delete", "children"]

    def get_children(self, obj):
        categories = {}
        for children in obj.children.all():
            categories = self.__class__(instance=children).data
        return categories


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = "__all__"


class ProductImageUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    # class Meta:
    #     model = Image
    #     fields = ('id', 'image',)
