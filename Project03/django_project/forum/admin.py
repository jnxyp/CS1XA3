from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

admin.site.register(Thread)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(ForumUser)