from rest_framework import status

from order_module.models import Order, OrderDetail
from product_module.models import Product


def is_valid_add_to_order(request, product_id, count):
    product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
    if product is not None and product.quantity >= count:
        current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
        current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
        if current_order_detail is not None:
            current_order_detail.count += count
            # if product.quantity > current_order_detail.count
            if True:
                current_order_detail.save()
                return {"res": {"detail": "با موفقیت به سبد خرید شما اضافه شد"}, "status": status.HTTP_200_OK,
                        "view_status": "success"}
            else:
                return {"res": {"detail": "مقدار انتخابی و یا داخل سبد خرید شما بیشتر از موجودی محصول میباشد"},
                        "status": status.HTTP_400_BAD_REQUEST, "view_status": "error"}
        else:
            new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
            new_detail.save()
        return {"res": {"detail": "با موفقیت به سبد خرید شما اضافه شد"}, "status": status.HTTP_200_OK,
                "view_status": "success"}
    else:
        return {"res": {"detail": "محصول مورد نظر یافت نشد یا موجودی کافی نیست"}, "status": status.HTTP_400_BAD_REQUEST,
                "view_status": "error"}
