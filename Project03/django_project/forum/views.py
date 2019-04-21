from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


# Index
def index(request):
    return HttpResponse('Index of Forum')


# Tag
def tag(request, tag_id: int):
    return HttpResponse('Threads with tag #%d of Forum' % tag_id)


# Thread
def thread(request, thread_id: int):
    return HttpResponse('Thread #%d' % thread_id)


# User
def user(request, user_id: int):
    return HttpResponse('User #%d' % user_id)
