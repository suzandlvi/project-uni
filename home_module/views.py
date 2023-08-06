from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import TemplateView

# Create your views here.
from order_module.models import OrderDetail
from product_module.models import Product


class HomeView(TemplateView):
    template_name = 'home_module/home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['new_products'] = Product.objects.all().order_by('-created_date')[:5]
        return context


def site_header_component(request):
    order_details_count = OrderDetail.objects.filter(order__user_id=request.user.id, order__is_paid=False).count()
    return render(request, 'shared/site_header_component.html', context={'order_details_count': order_details_count})
