from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ForumUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True,
                                related_name='forum_user', related_query_name='forum_user')
    nick_name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.nick_name)


class Post(models.Model):
    author = models.ForeignKey(to=ForumUser, on_delete=models.CASCADE, related_name='posts',
                               related_query_name='post', null=True)
    contents = models.TextField('Post Contents')
    pub_date = models.DateTimeField('Date Published')
    parent_thread = models.ForeignKey(to='Thread', on_delete=models.CASCADE, related_name='posts',
                                      related_query_name='post')
    reply_target = models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='replies', related_query_name='reply')

    def clean(self):
        super().clean()
        if self.reply_target:
            if self.parent_thread != self.reply_target.parent_thread:
                raise ValidationError(
                    'Reply target has different parent thread with current Post object')

    def __str__(self):
        return '%s: %s' % (self.author.nick_name, self.contents[:50])


class Category(models.Model):
    name = models.CharField('Tag Name', max_length=100)
    description = models.TextField('Tag Description', blank=True)

    def __str__(self):
        return str(self.name)


class Thread(models.Model):
    author = models.ForeignKey(to=ForumUser, on_delete=models.CASCADE, related_name='threads',
                               related_query_name='thread', null=True)
    title = models.CharField('Thread Title', max_length=100)
    pub_date = models.DateTimeField('Date Published')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='threads',
                                 related_query_name='thread', null=True)

    def __str__(self):
        return '%s: %s' % (self.author.nick_name, self.title[:50])
