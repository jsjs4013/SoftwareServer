"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 django에서 기본적으로 지원하는 admin사이트에 모델들을 적용시키는 파일이다.
"""

from django.contrib import admin
from snippets.models import User, UsedBook, Request, ChatList

admin.site.register(User)
admin.site.register(UsedBook)
admin.site.register(Request)
admin.site.register(ChatList)

# Register your models here.
