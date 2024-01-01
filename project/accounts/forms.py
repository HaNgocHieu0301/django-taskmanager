from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from .models import UserInfo
from .widgets import InputCustom
from django.utils.translation import gettext as _


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return mark_safe('<div class="text-xs italic text-red-700">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self]))

    def as_ul(self):
        if not self:
            return ''
        return mark_safe('<div class="text-xs italic text-red-700">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self]))


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        label=False,
        widget=InputCustom(attrs={
            'placeholder': 'Username',
            'title': 'Username',
            'type': 'text'
        }),
    )
    password = forms.CharField(
        required=True,
        label=False,
        widget=InputCustom(attrs={
            'placeholder': '••••••••',
            'title': 'Confirm Password',
            'type': 'password'
        }),
    )
    error_messages = {
        'invalid_login': _('Đăng nhập không thành công. \n Vui lòng kiểm tra lại thông tin.'),
        "inactive": _("This account is inactive."),
    }


class RegisterForm(ModelForm):
    re_password = forms.CharField(
        required=True,
        label=False,
        widget=InputCustom(attrs={'placeholder': '••••••••', 'title': 'Confirm Password', 'type': 'password'}),)

    class Meta:
        model = UserInfo
        fields = ['username', 'email', 'password', 're_password']
        widgets = {
            'username': InputCustom(attrs={'placeholder': 'UserName', 'title': 'Your Username'}),
            'email': InputCustom(attrs={'placeholder': 'abc@example.com', 'title': 'Your Email'}),
            'password': InputCustom(attrs={'placeholder': '••••••••', 'title': 'Your Password', 'type': 'password'}),
            're_password': InputCustom(attrs={'placeholder': '••••••••', 'title': 'Confirm Password', 'type': 'password'}),
        }
        labels = {
            'username': False,
            'password': False,
            'email': False,
            're_password': False
        }
        help_texts = {
            'username': False,
            'password': False,
            'email': False,
            're_password': False
        }

    def save(self, commit=True, *args, **kwargs):
        """
            hash password (may using _create_user)
        """
        m = super().save(commit=False)
        m.password = make_password(self.cleaned_data['password'])
        m.username = self.cleaned_data['username'].lower()
        if commit:
            m.save()
        return m

    def clean_email(self):
        email = self.cleaned_data['email']
        if email in UserInfo.objects.filter(email=email):
            raise ValidationError('Email already exists!')
        return email

    def clean_re_password(self):
        re_password = self.cleaned_data['re_password']
        password = self.cleaned_data['password']
        if not re_password:
            raise ValidationError('You must confirm password')
        if password != re_password:
            raise ValidationError('Confirm password must match with your password!')
