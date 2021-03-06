"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 django rest framework에서 url들의 처리를 담당하는 파일이다.
 jwt토큰인증 방식을 사용하기에 obtain_jwt_token, refresh_jwt_token 그리고 verify_jwt_token 클래스들을 사용하여 jwt토큰을 받아와 사용자 인증한다.
"""

from django.conf.urls import url, include
from snippets import views

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


urlpatterns = [
    url(r'^loginCheck/$', views.LoginCommit.as_view()),
    url(r'^signup/$', views.UserManage.as_view()),
    url(r'^receive/token/(?P<username>[0-9]+)/$', views.UserChange.as_view()),

    url(r'^loginCheck/(?P<my_parameter>.+)/(?P<my_parameters>.+)/$', views.TestLoginCommit.as_view()),

    url(r'^register/book/$', views.BookList.as_view()),
    url(r'^register/book/(?P<pk>[0-9]+)/$', views.BookDetail.as_view()),

    url(r'^application/book/$', views.BuyCheckBook.as_view()),
    url(r'^application/del/book/(?P<pk>[0-9]+)/$', views.BookCheckDetail.as_view()),

    url(r'^search/book/(?P<bookName>.+)/$', views.SearchBook.as_view()),
    url(r'^search/book/$', views.SearchBook.as_view()),

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/change/$', views.UserChange.as_view()),
    url(r'^users/(?P<username>[0-9]+)/my/register/book/$', views.MyBookList.as_view()),
    url(r'^users/(?P<username>[0-9]+)/my/request/book/$', views.MyRequestList.as_view()),
    url(r'^users/(?P<username>[0-9]+)/my/buy/book/(?P<bookId>[0-9]+)/$', views.MyBuyBook.as_view()),
    url(r'^users/(?P<username>[0-9]+)/my/chat/list/$', views.ChatListGETPOST.as_view()),
    url(r'^users/(?P<username>[0-9]+)/my/chat/list/partner/$', views.ChatListPartnerGETPOST.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/my/chat/list/update/$', views.ChatListDetail.as_view()),

    url(r'^test/$', views.TestCheck.as_view()),

    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]