from django.shortcuts import render

from .apps import ForumConfig

# Create your views here.

from django.http import HttpResponse
from django.views.generic import TemplateView, ListView


# Index


# def index(request):
#     return render(request, 'forum/header_and_footer.html')


class IndexPageView(TemplateView):
    template_name = 'forum/index.html'
    extra_context = {'auth_config': ForumConfig.__dict__,
                     'title': 'Index Page - %s' % ForumConfig.verbose_name}


class TagList(ListView):
    pass

# Tag
def tag(request, tag_id: int):
    return HttpResponse('Threads with tag #%d of Forum' % tag_id)


# Thread
def thread(request, thread_id: int):
    return HttpResponse('Thread #%d' % thread_id)


# User
def user(request, user_id: int):
    return HttpResponse('User #%d' % user_id)
