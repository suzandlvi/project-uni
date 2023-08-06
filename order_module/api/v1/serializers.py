from rest_framework import serializers
from order_module.models import *
from product_module.models import Product


class OrderSerializer(serializers.ModelSerializer):
    discount_price = serializers.IntegerField(source="get_discount_price")
    products_price = serializers.IntegerField(source="calculate_products_price")
    total_price = serializers.IntegerField(source="calculate_total_price")

    class Meta:
        model = Order
        fields = "__all__"


class OrderDetailProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True, required=False)

    class Meta:
        model = Product
        fields = ["title", "image", "price", "quantity", ]


class OrderDetailSerializer(serializers.ModelSerializer):
    product = OrderDetailProductSerializer()
    total_price = serializers.IntegerField(source="get_total_price")

    class Meta:
        model = OrderDetail
        fields = "__all__"


class OrderAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    count = serializers.IntegerField(min_value=1)


class ShipmentSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    national_code = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    province = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    house_number = serializers.CharField(required=False)
    building_unit = serializers.CharField(required=False)
    postal_code = serializers.CharField(required=True)
    address = serializers.CharField(required=True)

    def validate_national_code(self, value):
        res = is_valid_iran_code(value)
        if res:
            return value
        else:
            raise serializers.ValidationError("کد ملی وارد شده صحیح نمیباشد", code="bad_request")

    def validate_phone_number(self, value):
        res = is_valid_phone_number(value)
        if res:
            return value
        else:
            raise serializers.ValidationError("شماره موبایل وارد شده صحیح نمیباشد", code="bad_request")

    def validate_postal_code(self, value):
        # res = is_valid_postal_code(value)
        # if res:
        #     return value
        # else:
        #     raise forms.ValidationError("کد پستی وارد شده معتبر نمیباشد")
        return value
