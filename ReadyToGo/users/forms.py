from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField


User = get_user_model()


class CreationForm(UserCreationForm):

    username = forms.CharField(  
        max_length=150,  
        label='Имя пользователя',  
        widget=forms.TextInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите имя пользователя'  
        })  
    )  
    email = forms.EmailField(  
        widget=forms.EmailInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите email'  
        })  
    )  
    password1 = forms.CharField(  
        max_length=128,  
        label='Пароль',  
        widget=forms.PasswordInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите пароль'  
        })  
    )  
    password2 = forms.CharField(  
        max_length=128,  
        label='Подтверждение пароля',  
        widget=forms.PasswordInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Повторите пароль'  
        })  
    )
    captcha = ReCaptchaField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'password1', 'password2', 'captcha')
        # fields = ('first_name', 'last_name', 'username', 'email',
        #           'password1', 'captcha')