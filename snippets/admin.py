"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 django rest framework에서 model과 view사이의 연결통로 및 적절한 컨트롤러 역할을 한다.
 외래키의처리 데이터형식설정 create, update등 model과 view의 사이에서 적절한 다리역할을 한다.

 공통적으로 나타나는 클래스
 Meta class - 기본적인 반환형과 현재 serializer클래스가 사용하는 model을 설정한다.
"""

from django.contrib import admin
from snippets.models import User, UsedBook, Request, ChatList

admin.site.register(User)
admin.site.register(UsedBook)
admin.site.register(Request)
admin.site.register(ChatList)

# Register your models here.
