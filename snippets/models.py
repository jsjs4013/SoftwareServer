from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class UsedBook(models.Model):
    owner = models.ForeignKey('auth.User', related_name='books')

    created = models.DateTimeField(auto_now_add=True)
    bookTitle = models.CharField(max_length=100, blank=True, default='')
    author = models.CharField(max_length=100, blank=True, default='')
    publisher = models.CharField(max_length=100, blank=True, default='')
    isbn = models.CharField(max_length=100, blank=True, default='')
    cource = models.CharField(max_length=100, blank=True, default='')
    professor = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('created',)


class Request(models.Model):
    owner = models.ForeignKey('auth.User', related_name='requestbuyers')
    bookId = models.CharField(max_length=100, blank=True, default='')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)