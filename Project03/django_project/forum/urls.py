from django.urls import path

from . import views

urlpatterns = [
    # ex: /forum/
    path('', views.index, name='index'),
    # ex: /forum/tag/666
    path('tag/<int:tag_id>/', views.tag, name='detail'),
    # ex: /forum/thread/666/
    path('thread/<int:thread_id>/', views.thread, name='results'),
    # ex: /forum/user/666/
    path('user/<int:user_id>/', views.user, name='vote'),
]
