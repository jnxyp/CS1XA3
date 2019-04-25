from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    # ex: /forum/
    path('', views.IndexPageView.as_view(), name='index'),
    # ex: /forum/tag/666
    path('tag/<int:tag_id>/', views.tag, name='tag_detail'),
    path('tag/', views.tag, name='tag_list'),
    # ex: /forum/thread/666/
    path('thread/<int:thread_id>/', views.thread, name='thread'),
    # ex: /forum/user/666/
    path('user/<int:user_id>/', views.user, name='user_info'),
]
