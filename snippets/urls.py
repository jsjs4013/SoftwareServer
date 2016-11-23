from django.conf.urls import url, include
from snippets import views

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


urlpatterns = [
    url(r'^loginCheck/$', views.LoginCommit.as_view()),
    url(r'^signup/$', views.UserManage.as_view()),

    url(r'^register/book/$', views.BookList.as_view()),
    url(r'^register/book/(?P<pk>[0-9]+)/$', views.BookDetail.as_view()),

    url(r'^application/book/$', views.BuyCheckBook.as_view()),
    url(r'^application/del/book/(?P<pk>[0-9]+)/$', views.BookCheckDetail.as_view()),

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]