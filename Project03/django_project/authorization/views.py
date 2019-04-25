from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, resolve_url
from django.utils.http import is_safe_url
from django.views.generic import FormView, DetailView

from .apps import AuthConfig
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.

# def login(request):
#     if request.user.is_authenticated:
#         return redirect('authorization:index')
#
#     if request.method == "GET":
#         return render(request, 'authorization/login.html',
#                       context={'auth_config': AuthConfig.__dict__, 'request': request,
#                                'title': 'Login - %s' % AuthConfig.verbose_name})
#     elif request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = auth.authenticate(username=username, password=password)
#         if user is not None and user.is_active:
#             auth.login(request, user=user)
#             return redirect('authorization:index')
#         else:
#             return redirect('authorization:login')


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             return redirect("authorization:index")
#     else:
#         form = UserCreationForm()
#         return render(request, 'authorization/register.html',
#                       context={'auth_config': AuthConfig.__dict__, 'request': request,
#                                'title': 'Register - %s' % AuthConfig.verbose_name, 'form': form})

# def logout(request):
#     if not request.user.is_authenticated:
#         return redirect('authorization:login')
#
#     else:
#         auth.logout(request)
#         return redirect('authorization:index')

# def index(request):
#     return render(request, 'authorization/index.html',
#                       context={'auth_config': AuthConfig.__dict__,
#                                'title': 'Account Info - %s' % AuthConfig.verbose_name})

class ModifiedLoginView(LoginView):
    class BootstrapAuthenticationForm(AuthenticationForm):
        required_css_class = 'font-weight-bold'
        error_css_class = 'text-danger'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name in self.fields:
                self.fields[field_name].widget.attrs.update(
                    {'class': 'form-control',
                     'placeholder': 'Enter %s' % self.fields[field_name].label})

    redirect_authenticated_user = True
    form_class = BootstrapAuthenticationForm
    template_name = 'authorization/login.html'
    extra_context = {'auth_config': AuthConfig.__dict__,
                     'title': 'Login - %s' % AuthConfig.verbose_name}


class RegisterView(FormView):
    class BootstrapUserCreationForm(UserCreationForm):
        required_css_class = 'font-weight-bold'
        error_css_class = 'text-danger'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name in self.fields:
                self.fields[field_name].widget.attrs.update(
                    {'class': 'form-control',
                     'placeholder': 'Enter %s' % self.fields[field_name].label})

    template_name = 'authorization/register.html'
    form_class = BootstrapUserCreationForm
    extra_context = {'auth_config': AuthConfig.__dict__,
                     'title': 'Register - %s' % AuthConfig.verbose_name}

    # Using the redirect process methods defined in LoginView
    success_url_allowed_hosts = set()
    redirect_field_name = 'next'

    def get_redirect_url(self):
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, resolve_url('authorization:login'))
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts={self.request.get_host(), *self.success_url_allowed_hosts},
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_success_url(self):
        return self.get_redirect_url()

    def form_valid(self, form):
        # if the form is valid, save that user to DB
        form.save()
        # if the session is currently logged in, log it out after new account created
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().form_valid(form)


class ModifiedLogoutView(LogoutView):
    template_name = 'authorization/logged_out.html'
    extra_context = {'auth_config': AuthConfig.__dict__,
                     'title': 'Logged Out - %s' % AuthConfig.verbose_name}


class UserDetailView(DetailView):
    model = User
    template_name = 'authorization/index.html'
    extra_context = {'auth_config': AuthConfig.__dict__,
                     'title': 'Account Info - %s' % AuthConfig.verbose_name}

    # Override the default get_object function, since we just need to display the current User
    def get_object(self, queryset=None):
        return self.request.user
