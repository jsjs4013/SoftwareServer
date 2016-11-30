"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 django rest framework에서 model과 view사이의 연결통로 및 적절한 컨트롤러 역할을 한다.
 외래키의처리 데이터형식설정 create, update등 model과 view의 사이에서 적절한 다리역할을 한다.

 공통적으로 나타나는 클래스
 Meta class - 기본적인 반환형과 현재 serializer클래스가 사용하는 model을 설정한다.
"""

from django.db import models
from django.conf import settings
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from django.contrib.auth.models import AbstractUser

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, default='')
    token = models.TextField(blank=True, default='')


# class Profile(models.Model):
#     user = models.OneToOneField(User)
#     name = models.CharField(max_length=100, blank=True)


class UsedBook(models.Model):
    owner = models.ForeignKey(User, related_name='books')

    created = models.DateTimeField(auto_now_add=True)
    bookTitle = models.CharField(max_length=100, blank=True, default='')
    author = models.CharField(max_length=100, blank=True, default='')
    publisher = models.CharField(max_length=100, blank=True, default='')
    isbn = models.CharField(max_length=100, blank=True, default='')
    cource = models.CharField(max_length=100, blank=True, default='')
    professor = models.CharField(max_length=100, blank=True, default='')
    comment = models.TextField(blank=True, default='')
    status = models.CharField(max_length=100, blank=True, default='')
    price = models.CharField(max_length=100, blank=True, default='')
    sellerPrice = models.CharField(max_length=100, blank=True, default='')
    pubdate = models.CharField(max_length=100, blank=True, default='')
    image = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('created',)


class ChatList(models.Model):
    studentId = models.ForeignKey(User, related_name='chatLists')
    partner = models.CharField(max_length=100, blank=True, default='')
    partnerName = models.CharField(max_length=100, blank=True, default='')
    lastMessage = models.CharField(max_length=100, blank=True, default='')


class Request(models.Model):
    owner = models.ForeignKey(User, related_name='requestbuyers')
    ownerName = models.CharField(max_length=100, blank=True, default='')
    bookId = models.CharField(max_length=100, blank=True, default='')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)