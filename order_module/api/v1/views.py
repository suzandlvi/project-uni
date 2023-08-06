import datetime

from django.http import HttpRequest
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product_module.models import Product, ProductCoupon
from site_module.models import Province, City
from .permissions import OrderPermission
from .serializers import *
from ...valid_order import is_valid_add_to_order


class OrderAPIView(APIView):
    # serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    # permission_classes = [OrderPermission]

    class CouponSerializer(serializers.Serializer):
        coupon = serializers.CharField(max_length=10, required=True)

        # def validate_coupon(self, value):
        #     try:
        #         selected_coupon = ProductCoupon.objects.get(coupon_code__exact=value,
        #                                                     expires_date__gte=datetime.datetime.now())
        #     except ProductCoupon.DoesNotExist:
        #         raise serializers.ValidationError("کوپن وارد شده معتبر نمیباشد", code="bad_request")
        #     return value
        def validate(self, attrs):
            coupon_code = attrs["coupon"]
            try:
                selected_coupon = ProductCoupon.objects.get(coupon_code__exact=coupon_code,
                                                            expires_date__gte=datetime.datetime.now(
                                                                tz=datetime.timezone.utc))
            except ProductCoupon.DoesNotExist:
                raise serializers.ValidationError("کوپن وارد شده معتبر نمیباشد", code="bad_request")
            attrs["coupon_instance"] = selected_coupon
            return attrs

    @extend_schema(request=None, responses=OrderSerializer)
    def get(self, request: HttpRequest):
        order, created = Order.objects.get_or_create(user_id=request.user.id, is_paid=False)
        serializer = OrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=CouponSerializer, responses=OrderSerializer)
    def patch(self, request):
        serializer = self.CouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
        current_order.discount = serializer.validated_data["coupon_instance"]
        current_order.save()
        return Response(OrderSerializer(instance=current_order).data, status=status.HTTP_200_OK)


class OrderDetailAPIView(GenericAPIView):
    serializer_class = OrderDetailSerializer
    queryset = OrderDetail.objects.all()
    permission_classes = [IsAuthenticated]

    # permission_classes = [OrderPermission]

    def get(self, request: HttpRequest):
        order, created = Order.objects.get_or_create(user_id=request.user.id, is_paid=False)
        order_details = self.queryset.filter(order_id=order.id)
        serializer = self.serializer_class(instance=order_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderAddAPIView(GenericAPIView):
    serializer_class = OrderAddSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data.get('product_id')
        count = serializer.validated_data.get('count')
        res = is_valid_add_to_order(request, product_id, count)
        return Response(res["res"], status=res["status"])


class ShipmentAPIView(GenericAPIView):
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_order = Order.objects.prefetch_related('orderdetail_set').filter(is_paid=False).first()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        province = serializer.validated_data.pop("province")
        city = serializer.validated_data.pop("city")
        try:
            db_province = Province.objects.get(name=province)
            db_city = City.objects.get(name=city)
        except (Province.DoesNotExist, City.DoesNotExist) as e:
            return Response({"detail": "شهر یا استان انتخاب شده معتبر نمیباشد"}, status=status.HTTP_400_BAD_REQUEST)

        created_shipment = Shipment.objects.create(**serializer.validated_data, province_id=db_province.id,
                                                   city_id=db_city.id, user_id=request.user.id)
        current_order.shipment_id = created_shipment.id
        current_order.save()
        return Response({"detail": "با موفقیت اطلاعات گیرنده ثبت شد"}, status=status.HTTP_201_CREATED)
