from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, TemplateView, View

from .forms import CreationForm
from .task import activate_email_task


User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('signup_done')
    template_name = 'signup.html'
    extra_context = {'title': 'Регистрация на сайте'}

    def form_valid(self, form):  
        user = form.save()  
        user.is_active = False  
        user.save()  
        activate_email_task(user)  
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):  
        return self.success_url


class CustomRegistrationDoneView(TemplateView):  
    template_name = "users/signup_done.html"  
    extra_context = {"title": "Регистрация завершена, активируйте учётную запись."}


class CustomRegistrationConfirmView(View):  
    def get(self, request, uidb64, token):  
        try:  
            uid = urlsafe_base64_decode(uidb64)  
            user = User.objects.get(pk=uid)  
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
        if user is not None and default_token_generator.check_token(user, token):  
            user.is_active = True  
            user.save()  
            login(request, user)  
            return render(  
                request,  
                "users/signup_confirmed.html",  
                {"title": "Учётная запись активирована."},  
            )  
        else:  
            return render(  
                request,  
                "users/signup_not_confirmed.html",  
                {"title": "Ошибка активации учётной записи."},  
            )
