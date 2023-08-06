from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from contact_module.forms import ContactUsForm
from contact_module.models import ContactUs
from site_module.models import SiteSetting


class ContactUsView(LoginRequiredMixin,View):
    def get(self, request):
        context = {'site_setting': SiteSetting.objects.filter(is_main_setting=True).first(), 'form': ContactUsForm()}
        return render(request, 'contact_module/contact-us.html', context)

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            new_contact = form.save(commit=False)
            user_contacts = len(ContactUs.objects.filter(email__iexact=new_contact.email, is_read_by_admin=False))
            if user_contacts > 1:
                return JsonResponse({
                    'status': 'error', 'message': 'شما باید منتظر خوانده شدن پیام های قبلی تان از طرف ادمین باشید'
                })
            else:
                new_contact.save()
            return JsonResponse({'status': 'success',
                                 'message': 'پیام شما با موفقیت ارسال شد نتیجه در صورت نیاز از طریق ایمیل به دست شما '
                                            'میرسد'})
        else:
            error = 'مشکلی رخ داد'
            for field in form:
                if field.errors:
                    for error in field.errors:
                        error = error
            return JsonResponse({
                'status': 'error', 'message': error
            })
