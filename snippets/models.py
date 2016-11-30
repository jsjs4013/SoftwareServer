"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 장고 ORM을 사용하기 위한 모델 파일이다.
 클래스형식으로 데이터베이스를 만들 수 있다.
"""

from django.db import models
from django.conf import settings
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from django.contrib.auth.models import AbstractUser

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


# User모델을 커스텀해서 만든 모델이다.
class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, default='')
    token = models.TextField(blank=True, default='')


# class Profile(models.Model):
#     user = models.OneToOneField(User)
#     name = models.CharField(max_length=100, blank=True)


# 등록된 책을 위한 모델이다.
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


# 채팅메시지의 정보를 위한 모델이다.
class ChatList(models.Model):
    studentId = models.ForeignKey(User, related_name='chatLists')
    studentName = models.CharField(max_length=100, blank=True, default='')
    partner = models.CharField(max_length=100, blank=True, default='')
    partnerName = models.CharField(max_length=100, blank=True, default='')
    lastMessage = models.CharField(max_length=100, blank=True, default='')


# 요청을 위한 메서드이다.
class Request(models.Model):
    owner = models.ForeignKey(User, related_name='requestbuyers')
    ownerName = models.CharField(max_length=100, blank=True, default='')
    bookId = models.CharField(max_length=100, blank=True, default='')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)