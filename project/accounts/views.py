from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import models
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import RegisterForm, LoginForm, DivErrorList
from .models import UserInfo


class SignUp(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = 'accounts/signup.html'

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        # Logic xử lý khi form không hợp lệ
        return self.render_to_response(self.get_context_data(form=form))

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.POST or None, error_class=DivErrorList)

    # def form_valid(self, form):
    #     # remember_me = form.cleaned_data.get('remember_me')
    #     # if not remember_me:
    #     #     self.request.session.set_expiry(0)
    #     # else:
    #     self.request.session.set_expiry(60*30)
    #     return super(CustomLoginView, self).form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = '/login'
