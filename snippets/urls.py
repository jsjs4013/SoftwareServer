# from django.conf.urls import url
# #from rest_framework.urlpatterns import format_suffix_patterns
# from snippets import views
# from django.conf.urls import include
#
# #from snippets.views import SnippetViewSet, UserViewSet, api_root
# #from rest_framework import renderers
#
# from rest_framework.routers import DefaultRouter
#
#
# # 라우터를 생성하고 뷰셋을 등록합니다
# router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet)
# router.register(r'loginCommit', views.LoginCommit)
# router.register(r'users', views.UserViewSet)
#
# # 이제 API URL을 라우터가 자동으로 인식합니다
# # 추가로 탐색 가능한 API를 구현하기 위해 로그인에 사용할 URL은 직접 설정을 했습니다
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]
#
#
# # snippet_list = SnippetViewSet.as_view({
# #     'get': 'list',
# #     'post': 'create'
# # })
# # snippet_detail = SnippetViewSet.as_view({
# #     'get': 'retrieve',
# #     'put': 'update',
# #     'patch': 'partial_update',
# #     'delete': 'destroy'
# # })
# # snippet_highlight = SnippetViewSet.as_view({
# #     'get': 'highlight'
# # }, renderer_classes=[renderers.StaticHTMLRenderer])
# # user_list = UserViewSet.as_view({
# #     'get': 'list'
# # })
# # user_detail = UserViewSet.as_view({
# #     'get': 'retrieve'
# # })
# #
# # urlpatterns = [
# #     url(r'^$', views.api_root),
# #     url(r'^snippets/$', snippet_list, name='snippet-list'),
# #     url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
# #     url(r'^users/$', user_list, name='user-list'),
# #     url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
# #     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
# # ]
# #
# # urlpatterns = format_suffix_patterns(urlpatterns)
# #
# # urlpatterns += [
# #     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
# # ]

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^loginCheck/$', views.LoginCommit.as_view()),
    #url(r'^loginCheck/(?P<id>\d+)/(?P<pw>[a-z0-9]+)/$', views.LoginCommit.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)