from django.urls import path
from . import views

app_name = 'authorization'

urlpatterns = [
    path('login/', views.ModifiedLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.ModifiedLogoutView.as_view(), name='logout'),
    path('', views.UserDetailView.as_view(), name='index'),
]
