import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpRequest, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
# Create your views here.
from django.utils.safestring import mark_safe
from django.views import View

from order_module.forms import ShipmentForm
from order_module.models import Order, OrderDetail, Shipment
from order_module.valid_order import is_valid_add_to_order
from product_module.models import Product, ProductCoupon
from site_module.models import Province, City


class CartView(LoginRequiredMixin, View):
    def total_price(self, order_detail, request):
        order = Order.objects.get(is_paid=False, user_id=request.user.id)
        total = order_detail.get_total_price()
        total_products = order.calculate_products_price
        total_amount = order.calculate_total_price()
        return total, total_amount, total_products

    def get(self, request):
        current_order, created = Order.objects.prefetch_related('orderdetail_set',
                                                                'orderdetail_set__product').get_or_create(is_paid=False,
                                                                                                          user_id=request.user.id)
        total_amount = current_order.calculate_products_price
        context = {
            'order': current_order,
            'sum': total_amount,
            'sum_plus': current_order.calculate_total_price() + 15000,
        }
        return render(request, 'order_module/cart.html', context)

    def post(self, request):
        request_type = request.POST.get('type')
        if request_type == 'coupon':
            order = Order.objects.get(is_paid=False, user_id=request.user.id)
            order_coupon = ProductCoupon.objects.filter(coupon_code__exact=request.POST.get('coupon_code'),
                                                        expires_date__gte=datetime.datetime.now(tz=datetime.timezone.utc))
            if order_coupon.exists():
                order.discount = order_coupon.first()
                order.save()
                total_amount = order.calculate_total_price()
                return JsonResponse(
                    {'status': 'success', 'total_amount': total_amount, 'discount_price': order.get_discount_price,
                     'message': 'کد تخفیف شما با موفقیت اعمال شد'})
            else:
                return JsonResponse(
                    {'status': 'error', 'message': 'کد تخفیف وارد شده یافت نشد'})
        order_detail_id = request.POST.get('order_detail_id')
        order_detail = OrderDetail.objects.get(id=order_detail_id, order__user_id=request.user.id)
        if request_type == 'reduce':
            if order_detail.count == 1:
                return JsonResponse({'status': 'error'})
            order_detail.count -= 1
            order_detail.save()
            total, total_amount, total_products = self.total_price(order_detail, request)
            total = str(total)
            return JsonResponse(
                {'status': 'success', 'total': total, 'total_products': total_products, 'total_amount': total_amount})
        elif request_type == 'add':
            order_detail.count += 1
            order_detail.save()
            total, total_amount, total_products = self.total_price(order_detail, request)
            return JsonResponse(
                {'status': 'success', 'total_products': total_products, 'total': total, 'total_amount': total_amount})
        elif request_type == 'delete':
            order_detail.delete()
            total, total_amount, total_products = self.total_price(order_detail, request)
            return JsonResponse(
                {'status': 'success', 'total': total, 'total_products': total_products, 'total_amount': total_amount,
                 'message': 'محصول مورد نظر شما با موفقیت حذف شد'})
        else:
            return JsonResponse({'status': 'error'})


@require_POST
def add_product_to_order(request: HttpRequest):
    product_id = int(request.POST.get('product_id'))
    count = int(request.POST.get('count'))
    if count < 1:
        # count = 1
        return JsonResponse({
            'status': 'error',
            'message': 'مقدار وارد شده معتبر نمی باشد',
        })

    if request.user.is_authenticated:
        res = is_valid_add_to_order(request, product_id, count)
        return JsonResponse({'status': res["view_status"], "message": res["res"]["detail"]})
    else:
        return JsonResponse({'status': "error", "message": "لطفا ابتدا لاگین کنید"})


class ShipmentView(LoginRequiredMixin, View):

    def get(self, request):
        current_order = Order.objects.prefetch_related('orderdetail_set').filter(is_paid=False).first()
        if not current_order.orderdetail_set.first():
            return HttpResponseForbidden("ابتدا باید محصولی را به سبد خرید خود اضافه کنید")
        return render(request, 'order_module/shipment.html')

    def post(self, request):
        current_order = Order.objects.prefetch_related('orderdetail_set').filter(is_paid=False).first()
        form = ShipmentForm(request.POST)
        if form.is_valid():
            province = form.cleaned_data.pop("province")
            city = form.cleaned_data.pop("city")
            try:
                db_province = Province.objects.get(name=province)
                db_city = City.objects.get(name=city)
            except (Province.DoesNotExist, City.DoesNotExist) as e:
                return render(request, 'order_module/shipment.html',
                              context={"error": "شهر یا استان انتخاب شده معتبر نمیباشد", "error_field": "none_field"})

            created_shipment = Shipment.objects.create(**form.cleaned_data, province_id=db_province.id,
                                                       city_id=db_city.id, user_id=request.user.id)
            current_order.shipment_id = created_shipment.id
            current_order.save()
            return redirect(reverse('cart_view'))
        else:
            error = 'مشکلی رخ داد'
            error_field = "none_field"
            for field in form:
                if field.errors:
                    for error in field.errors:
                        error = error
                        error_field = field.html_initial_id.replace("initial-id_", "")
            return render(request, 'order_module/shipment.html', context={"error": error, "error_field": error_field})
