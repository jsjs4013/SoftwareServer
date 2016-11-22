# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
#
#
# class SnippetList(APIView):
#     """
#         코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
#     """
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class SnippetDetail(APIView):
#     """
#         코드 조각 조회, 업데이트, 삭제
#     """
#
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#
#         return Response(status=status.HTTP_204_NO_CONTENT)

# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import mixins
# from rest_framework import generics
#
#
# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
# from snippets.loginCommit import EclassCheck
from rest_framework import generics, permissions, renderers, viewsets
# from django.contrib.auth.models import User
from snippets.permissions import IsOwnerOrReadOnly
#
# from rest_framework.decorators import api_view, detail_route
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
#
#
# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'snippets': reverse('snippet-list', request=request, format=format)
#     })


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#         이 뷰셋은 `list`와 `detail` 기능을 자동으로 지원합니다
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class SnippetList(generics.ListCreateAPIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

# class SnippetViewSet(viewsets.ModelViewSet):
#     """
#         이 뷰셋은 `list`와 `create`, `retrieve`, `update`, 'destroy` 기능을 자동으로 지원합니다
#
#         여기에 `highlight` 기능의 코드만 추가로 작성했습니다
#     """
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
#
#     @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
#     def highlight(self, request, *args, **kwargs):
#         snippet = self.get_object()
#
#         return Response(snippet.highlighted)
#
#     def perform_create(self, serializer):
#             serializer.save(owner=self.request.user)
#
# class LoginCommit(viewsets.ModelViewSet):
#     # def get(self, request, format=None):
#     #     snippets = Snippet.objects.all()
#     #     serializer = SnippetSerializer(snippets, many=True)
#     #     loginCheck = EclassCheck()
#     #     userName = loginCheck.check()
#     #
#     #     if userName != False:
#     #         return Response(loginCheck)
#
#
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
#
#     @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
#     def loginChecker(self, request, *args, **kwargs):
#         loginCheck = EclassCheck()
#         userName = loginCheck.check()
#
#         if userName != False:
#             return Response('success')

# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from snippets.loginCommit import EclassCheck
#
#
# @api_view(['GET', 'POST'])
# def snippet_list(request):
#     """
#     코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET'])
# def loginCommit(request):
#     """
#     코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
#     """
#     if request.method == 'GET':
#         loginCheck = EclassCheck()
#         userName = loginCheck.check()
#
#         if userName != False:
#             del loginCheck
#
#             return Response(userName)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk):
#     """
#     코드 조각 조회, 업데이트, 삭제
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer, ChangePasswordSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, authentication
from snippets.loginCommit import EclassCheck

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from snippets.utils import checkUser

from snippets.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User

from rest_framework_jwt import authentication
from rest_framework.generics import CreateAPIView, UpdateAPIView


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserManage(CreateAPIView):

    model = User
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if self.object.check_password(serializer.data.get("old_password")):
                return Response("No change.", status=status.HTTP_200_OK)
                # return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetList(APIView):
    """
    코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
    """
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
        # return Response(User.objects.values())

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ///////////////////////////////////////////////////////////////////
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    콘텐츠를 JSON으로 변환한 후 HttpResponse 형태로 반환합니다.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
# ///////////////////////////////////////////////////////////////////
# class UserManagement():
#     def login(self, ID, PW):
#         # User.objects.get(username="2014112022").delete()
#         try:
#             user = User.objects.get(username=ID)
#
#             if not user.check_password(PW):
#                 user.set_password(PW)
#                 user.save()
#         except User.DoesNotExist:
#             user = User(username=ID)
#             user.set_password(PW)
#             user.save()


class LoginCommit(APIView):
    def post(self, request, format=None):
        ID = request.POST["ID"]
        # PW = request.POST["PW"]
        PW = "mjw!112415"
        # user = UserManagement()

        loginCheck = EclassCheck()
        userName = loginCheck.check(ID, PW)
        i = 0

        while userName == False:
            userName = loginCheck.check(ID, PW)
            i += 1

            if i == 10:
                # user.login(ID, PW)
                return Response('error')

        # return JSONResponse(userName)
        # user.login(ID, PW)
        try:
            User.objects.get(username=ID)

            return Response({'username':userName, 'overlap':1})
        except User.DoesNotExist:
            return Response({'username':userName, 'overlap':0})

class SnippetDetail(APIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """
    # authentication_classes = (authentication.JSONWebTokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # def get_object(self, queryset=None):
    #     obj = self.request.user
    #     return obj

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        permission = checkUser()
        return permission.permissionGet(snippet, self.request.user)

        # serializer = SnippetSerializer(snippet)
        # return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        permission = checkUser()
        return permission.permissionPut(snippet, request.data, self.request.user)

        # if snippet.owner == self.request.user:
        #     serializer = SnippetSerializer(snippet, data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #
        # raise Http404

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        permission = checkUser()
        return permission.permissionDel(snippet, self.request.user)

        # snippet.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)