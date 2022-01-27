import math

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import  mark_safe
from django.utils.text import Truncator
from markdown import markdown


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_topics_count(self):
        return Topic.objects.filter(board=self).count()

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

    def get_newest_topic(self):
         return  Topic.objects.filter(board=self).order_by('-created_at').first()

    def get_newest_topic_subject(self):
        subject=Topic.objects.filter(board=self).order_by('-last_updated').first().subject
        return Truncator(subject).chars(15)




class Topic(models.Model):

    board = models.ForeignKey(Board, related_name='topics',on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    starter = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_last_ten_posts(self):
        return Post.objects.filter(topic=self).order_by('-created_at')[:10]

    def get_replies_count(self):
        posts_num=Post.objects.filter(topic=self).count()
        if posts_num>0:
            return posts_num-1
        else:
            return 0


    def get_last_updated(self):
        return Post.objects.filter(topic=self).order_by('-created_at').first()

    def get_page_count(self):
        from .views import EACH_PAGE_POSTS_NUM
        count = self.posts.count()
        pages=count/EACH_PAGE_POSTS_NUM
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)



class Post(models.Model):
    topic = models.ForeignKey(Topic,models.CASCADE,related_name='posts')
    message = models.TextField(max_length=4000)
    created_by = models.ForeignKey(User, models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='+')


    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    # def get_message_as_markdown(self):
    #     return mark_safe(markdown(str(self.message)))