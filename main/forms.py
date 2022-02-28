from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django import forms
from main.models import Product, ConfirmCode
from django.contrib.auth.models import User
from django.conf import settings
import secrets


class RegisterForm(forms.Form):
    username = forms.CharField(label='Пользователь', min_length=4, max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': "Enter your email"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))
    password2 = forms.CharField(label='Потвердить пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Repeat your password'
    }))


    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.filter(username=username)
        if users.count() > 0:
            raise ValidationError('User with this username already exists!')
        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise ValidationError('Password not match')
        return password

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            is_active=False

        )
        code = secrets.token_hex(10)
        ConfirmCode.objects.create(user=user, code=code)
        send_mail(
            subject='Confirmation message',
            message='',
            html_message=f'<a href="http://localhost:8000/confirm/?code={code}">Confirm please</a>',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.cleaned_data['email']],
            fail_silently=False
        )
        return user



class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        #fields = '__all__' # можно выбрать автоматом все характеристики
        fields = ['title', 'category', 'price', 'description', 'size', 'date_end'] # можно выбрать отдельно каждую характеристику

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a title',
                                            'class': 'form-control'}),
            'category': forms.Select(attrs={'placeholder': 'Enter a category',
                                            'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter a price',
                                            'class': 'form-control'}),
            'description': forms.TextInput(attrs={'placeholder': 'Enter a description',
                                            'class': 'form-control'}),
            'size': forms.TextInput(attrs={'placeholder': 'Enter a size',
                                            'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'placeholder': 'Enter a date_end',
                                            'class': 'form-control'}),
        }