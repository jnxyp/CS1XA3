from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ForumUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True)
    nick_name = models.CharField(max_length=30)



class Post(models.Model):
    author = models.ForeignKey(to=ForumUser, on_delete=models.CASCADE, related_name='posts',
                               related_query_name='post', null=True)
    contents = models.TextField('Post Contents')
    pub_date = models.DateTimeField('Date Published')
    parent_thread = models.ForeignKey(to='Thread', on_delete=models.CASCADE, related_name='posts',
                                      related_query_name='post')
    # TODO Limit the choice of reply target to the posts under the same thread
    reply_target = models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='replies', related_query_name='reply')


class Thread(models.Model):
    author = models.ForeignKey(to=ForumUser, on_delete=models.CASCADE, related_name='threads',
                               related_query_name='thread', null=True)
    title = models.CharField('Thread Title', max_length=100)


class Tag(models.Model):
    name = models.CharField('Tag Name', max_length=100)
    description = models.TextField('Tag Description', blank=True)
    posts = models.ManyToManyField(to='Thread')
