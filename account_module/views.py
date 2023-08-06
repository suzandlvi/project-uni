from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView
import weasyprint

from account_module.forms import RegisterForm, LoginForm, EditUserInfoForm, EditUserPasswordForm
from account_module.models import User
from order_module.models import Order
from utils.normalize_email import normalize_email


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home_view'))
        context = {'form': RegisterForm()}
        return render(request, 'account_module/register.html', context)

    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect(reverse('home_view'))
        form = RegisterForm(request.POST)
        if form.is_valid():
            created_user: User = form.save(commit=False)
            created_user.username = normalize_email(form.cleaned_data.get('email'))
            created_user.set_password(form.cleaned_data.get('password'))
            created_user.save()
            return JsonResponse(
                {'status': 'success', 'message': 'اکانت شما با موفقیت ساخته شد در حال تغییر مسیر به صفحه ورود'})
        else:
            error = 'مشکلی رخ داد'
            for field in form:
                if field.errors:
                    for error in field.errors:
                        error = error
            return JsonResponse({
                'status': 'error', 'message': error
            })


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home_view'))
        context = {'form': LoginForm()}
        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect(reverse('home_view'))
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=normalize_email(form.cleaned_data.get('email')),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect(request.POST.get('next', '/'))
            else:
                form.add_error('email', 'کاربری با مشخصات زیر یافت نشد')
                return render(request, 'account_module/login.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('home_view'))
        logout(request)
        return redirect(reverse('login_view'))


class UserPanel(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        context = {'user': user}
        return render(request, 'account_module/user_panel.html', context)


class OrderHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.prefetch_related('orderdetail_set', 'orderdetail_set__product').filter(
            user_id=request.user.id,
            is_paid=True)
        context = {'orders': orders}
        return render(request, 'account_module/order_history.html', context)


class EditUserInfoView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditUserInfoForm
    template_name = 'account_module/edit_user_info.html'
    success_url = reverse_lazy('user_panel_view')
    context_object_name = 'form'

    def get_object(self, queryset=None):
        user = User.objects.get(id=self.request.user.id)
        return user


class EditUserPasswordView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest):
        user: User = User.objects.get(id=request.user.id)
        form = EditUserPasswordForm()
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'account_module/edit_user_password.html', context)

    def post(self, request: HttpRequest):
        form = EditUserPasswordForm(data=request.POST)
        user: User = User.objects.get(id=request.user.id)
        if form.is_valid():
            if user.check_password(form.cleaned_data.get('current_password')):
                user.set_password(form.cleaned_data.get('new_password'))
                user.save()
                return redirect(reverse('user_panel_view'))
            else:
                form.add_error('current_password', 'کلمه عبور وارد شده اشتباه می باشد')
        return render(request, 'account_module/edit_user_password.html', {'user': user, 'form': form})


class OrderHistoryExportView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        try:
            order = Order.objects.prefetch_related('orderdetail_set', 'orderdetail_set__product').get(id=order_id,
                                                                                                      is_paid=True)
        except Order.DoesNotExist:
            return Http404('سفارش مورد نظر یافت نشد')
        html_file = render_to_string('account_module/components/pdf.html', context={'order': order})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'order-{order.id}'
        weasyprint.HTML(string=html_file).write_pdf(response, stylesheets=[weasyprint.CSS(
            str(settings.STATICFILES_DIRS[0]) + '/css/pdf.css'
        )])
        return response
