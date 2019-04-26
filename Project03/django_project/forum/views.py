from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .apps import ForumConfig
from .models import *

# Create your views here.

from django.http import HttpResponse
from django.views.generic import TemplateView, ListView


# Index


# def index(request):
#     return render(request, 'forum/header_and_footer.html')


class IndexPageView(ListView):
    template_name = 'forum/index.html'
    extra_context = {'auth_config': ForumConfig.__dict__,
                     'title': 'Index Page - %s' % ForumConfig.verbose_name}
    model = Thread
    paginate_by = 100

    def get_queryset(self):
        return Thread.objects.all()[::-1]


class CategoryList(ListView):
    template_name = 'forum/category_listing.html'
    extra_context = {'auth_config': ForumConfig.__dict__,
                     'title': 'Categories - %s' % ForumConfig.verbose_name}

    model = Category
    paginate_by = 100


def register_user(request):
    user = request.user
    if request.user.is_authenticated:
        try:
            user.forum_user is None
        except ForumUser.DoesNotExist:
            forum_user = ForumUser(user=user,
                                   nick_name=request.user.username)
            forum_user.save()
        return redirect('forum:index')
    else:
        return redirect('authorization:login')


# Tag
def category(request, category_id: int):
    category = Category.objects.get(pk=category_id)
    threads = category.threads.all()

    return render(request, 'forum/category_detail.html',
                  context={'category': category, 'object_list': threads,
                           'auth_config': ForumConfig.__dict__,
                           'title': '%s - Categories - %s' % (
                               category.name, ForumConfig.verbose_name)})


# Thread
def thread(request, thread_id: int):
    thread = Thread.objects.get(pk=thread_id)
    posts = thread.posts.all()

    return render(request, 'forum/thread_detail.html',
                  context={'thread': thread, 'object_list': posts,
                           'auth_config': ForumConfig.__dict__,
                           'title': '%s - Posts - %s' % (thread.title, ForumConfig.verbose_name)})


# User
def user(request, user_id: int):
    user = User.objects.get(pk=user_id)
    forum_user = user.forum_user
    threads = forum_user.threads.all()
    posts = forum_user.posts.all()

    return render(request, 'forum/user_detail.html',
                  context={'current_user': user, 'threads': threads, 'posts': posts,
                           'auth_config': ForumConfig.__dict__,
                           'title': '%s - Users - %s' % (
                               forum_user.nick_name, ForumConfig.verbose_name)})


@login_required
def create_thread(request):
    if request.method == 'POST':
        category_id = int(request.POST['thread-category'])
        title = request.POST['thread-title']
        contents = request.POST['thread-contents']

        thread_obj = Thread(author=request.user.forum_user, title=title, pub_date=datetime.now(),
                            category=Category.objects.get(pk=category_id))
        thread_obj.save()

        post = Post(author=request.user.forum_user, contents=contents, pub_date=datetime.now(),
                    parent_thread=thread_obj)
        post.save()

        return redirect('forum:thread', thread_id=thread_obj.id)
    else:
        try:
            category_id = int(request.GET.get('category_id'))
        except Exception:
            category_id = 1
        categories = Category.objects.all()
        return render(request, 'forum/create_thread.html',
                      context={'categories': categories,
                               'category_id': category_id,
                               'auth_config': ForumConfig.__dict__,
                               'title': 'Start new Thread - %s' % ForumConfig.verbose_name})


def create_reply(request):
    if request.method == 'POST':
        thread_id = int(request.POST['thread-id'])
        reply_target_id = int(request.POST['reply-target-id'])
        contents = request.POST['thread-contents']

        print(contents)

        post = Post(author=request.user.forum_user, contents=contents, pub_date=datetime.now(),
                    parent_thread_id=thread_id, reply_target_id=reply_target_id)
        post.save()

        return redirect('forum:thread', thread_id=thread_id)
    else:
        try:
            thread_id = int(request.GET.get('thread-id'))
            thread_obj = Thread.objects.get(pk=thread_id)
        except Exception:
            return redirect('forum:index')
        try:
            reply_target_id = int(request.GET.get('reply-target-id'))
        except Exception:
            reply_target_id = None
        return render(request, 'forum/create_reply.html',
                      context={'thread': thread_obj, 'reply_target_id': reply_target_id,
                               'auth_config': ForumConfig.__dict__,
                               'title': 'Reply to post #%d - %s' % (
                                   reply_target_id, ForumConfig.verbose_name)})
