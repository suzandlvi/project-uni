import time

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, View, DetailView

from order_module.models import Order
from product_module.models import Product, ProductBrand, ProductGallery, ProductComment, ProductVote, ProductCategory, \
    TestDownload
from product_module.recommender import Recommender


class ProductListView(View):
    def get(self, request, cat=None):
        products = Product.objects.filter(is_delete=False, is_active=True).order_by('-created_date')
        products = self.filter(request, products, cat)
        products = self.pagination(request, products)
        categories = ProductCategory.objects.filter(is_active=True, is_delete=False, parent=None)
        context = {'products': products, 'brands': ProductBrand.objects.filter(is_active=True),
                   'categories': categories}
        return render(request, 'product_module/products_list.html', context=context)

    def filter(self, request, products, cat=None):
        if cat is not None:
            products = products.filter(Q(category__slug__iexact=cat) | Q(category__parent__slug__iexact=cat) | Q(
                category__parent__parent__slug__iexact=cat))
        if request.GET.get('brand'):
            products = products.filter(brand__english_title=request.GET.get('brand'))
        search = request.GET.get('search')
        if search:
            products = products.filter(Q(title__contains=search) | Q(brand__english_title__contains=search) | Q(
                brand__title__contains=search) |
                                       Q(category__title__contains=search))
        if request.GET.get('available-checkbox') and request.GET.get('available-checkbox') == 'true':
            products = products.filter(quantity__gt=0)
        return products

    def pagination(self, request, products):
        paginator = Paginator(products, 5)  # Show 25 contacts per page.
        page_number = request.GET.get('page', 1)
        products = paginator.get_page(page_number)
        return products


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_module/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product: Product = context.get('product')
        context['gallery'] = ProductGallery.objects.filter(product_id=product.id)
        context['comments'] = ProductComment.objects.filter(product_id=product.id, is_accepted=True).order_by(
            '-create_date')
        context['order'] = Order.objects.prefetch_related('orderdetail_set').filter(user_id=self.request.user.id,
                                                                                    is_paid=False,
                                                                                    orderdetail__product_id=product.id)
        context['related_products'] = Product.objects.filter(
            Q(brand__title__iexact=product.brand.title) | Q(
                category__title__iexact=product.category.title)).exclude(id=product.id)
        # recommender = Recommender()
        # context['related_products'] = recommender.suggest_products_for([product], 6)
        if self.request.user.is_authenticated:
            try:
                user_vote = ProductVote.objects.get(user_id=self.request.user,
                                                    product_id=product.id)
                user_vote = user_vote.vote
            except ProductVote.DoesNotExist:
                user_vote = 0
            context['user_vote'] = user_vote
        return context

    def post(self, request: HttpRequest, slug):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'شما ابتدا باید در حساب کاربری خود لاگین کنید'})
        try:
            product = Product.objects.get(slug__iexact=slug)
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'محصول مورد نظر شما یافت نشد'})
        if request.POST.get('star'):
            try:
                recent_vote = ProductVote.objects.get(product_id=product.id, user_id=request.user.id)
                recent_vote.vote = request.POST.get('star')
                recent_vote.save()
            except ProductVote.DoesNotExist:
                ProductVote.objects.create(product_id=product.id, user_id=request.user.id,
                                           vote=request.POST.get('star'))
            time.sleep(1)
            vote_avg = product.vote_avg()
            return JsonResponse({'status': 'success', 'message': 'امتیاز شما ثبت شد', 'vote_avg': vote_avg})
        user_commends = ProductComment.objects.filter(user_id=request.user.id, product_id=product.id,
                                                      is_accepted=False).count()
        if user_commends > 2:
            return JsonResponse({'status': 'error',
                                 'message': 'بیشتر از این تعدا کامنت نمیتوانید ثبت کنید باید منتظر تایید نظر های قبلی تان باشید'})
        commend_text = request.POST.get('commend_text')
        commend_mode = request.POST.get('idea')
        if commend_mode is None or commend_mode is None:
            return JsonResponse({'status': 'error', 'message': 'حتما باید یک نظر و یک مود ثبت کنید'})
        ProductComment.objects.create(product_id=product.id, user_id=request.user.id,
                                      commend_mode=commend_mode, commend_text=commend_text)
        time.sleep(1)
        return JsonResponse(
            {'status': 'success', 'message': 'نظر شما با موفقیت ثبت شد بعد از تایید ادمین در سایت قرار میگیرد'})


class TestDownloadView(View):
    def get(self, request):
        # return render(request, 'product_module/test.html')
        # test = TestDownload.objects.first()
        # return FileResponse(test.file, as_attachment=True)
        test = TestDownload.objects.get(id=1)
        response = HttpResponse(test.file.read(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename={0}'.format("Export.rar")
        return response

    def post(self, request):
        test = TestDownload.objects.first()
        print('aha')
        return FileResponse(test.file, as_attachment=True)


# class Test(View):
#     def get(self, request):
#         return render(request, 'product_module/test.html')
#
#     def post(self, request):
#         test = TestDownload.objects.first()
#         print('aha')
#         return FileResponse(test.file, as_attachment=True)


# class Test(View):
#     def get(self, request):
#         return render(request, 'product_module/test.html')
#
#     def post(self, request):
#         test = TestDownload.objects.get(id=1)
#         response = HttpResponse(test.file.read(), content_type="application/zip")
#         response['Content-Disposition'] = 'attachment; filename={0}'.format("Export.rar")
#         return response
class Test(View):
    def get(self, request):
        return render(request, 'product_module/test1.html')

    def post(self, request):
        test = TestDownload.objects.get(id=1)
        response = HttpResponse(test.file.read(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename={0}'.format("Export.rar")
        return response
