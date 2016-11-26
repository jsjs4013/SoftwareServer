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
    comment = models.TextField()
    status = models.CharField(max_length=100, blank=True, default='')
    price = models.CharField(max_length=100, blank=True, default='')
    sellerPrice = models.CharField(max_length=100, blank=True, default='')
    pubdate = models.CharField(max_length=100, blank=True, default='')
    image = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('created',)


class Request(models.Model):
    owner = models.ForeignKey(User, related_name='requestbuyers')
    bookId = models.CharField(max_length=100, blank=True, default='')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)