from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    # ex: /forum/
    path('', views.IndexPageView.as_view(), name='index'),
    # ex: /forum/tag/666
    path('category/<int:category_id>', views.category, name='category_detail'),
    path('category/', views.CategoryList.as_view(), name='category_list'),
    # ex: /forum/thread/666/
    path('thread/<int:thread_id>', views.thread, name='thread'),
    # ex: /forum/user/666/
    path('user/<int:user_id>', views.user, name='user_info'),
    path('activate/', views.register_user, name='activate'),

    path('create/', views.create_thread, name='create_thread'),
    path('reply/', views.create_reply, name='create_reply')
]
