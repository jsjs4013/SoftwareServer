from snippets.models import User, UsedBook, Request
from snippets.serializers import UserSerializer, UsedBookSerializer, RequestSerializer
from django.http import Http404
from django.db.models import query
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, authentication
from snippets.loginCommit import EclassCheck

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from snippets.permissions import IsOwnerOrReadOnly, checkUser

from rest_framework_jwt import authentication
from rest_framework.generics import CreateAPIView, UpdateAPIView

import json


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


class LoginCommit(APIView):
    def post(self, request, format=None):
        received_json_data = json.loads(request.body.decode("utf-8"))
        ID = received_json_data['ID']
        PW = received_json_data['PW']

        # ID = request.POST['ID']
        # PW = request.POST['PW']

        # return Response((ID, PW))

        loginCheck = EclassCheck()
        userName = loginCheck.check(ID, PW)
        del loginCheck
        i = 0

        while userName == False:
            loginCheck = EclassCheck()
            userName = loginCheck.check(ID, PW)
            del loginCheck
            i += 1

            if i == 10:
                return Response('error')
        try:
            User.objects.get(username=ID)

            return Response({'username':userName, 'overlap':1})
        except User.DoesNotExist:
            return Response({'username':userName, 'overlap':0})


class TestLoginCommit(APIView):
    def get(self, request, my_parameter, my_parameters, format=None):
        ID = my_parameter
        PW = my_parameters

        loginCheck = EclassCheck()
        userName = loginCheck.check(ID, PW)
        del loginCheck
        i = 0

        while userName == False:
            loginCheck = EclassCheck()
            userName = loginCheck.check(ID, PW)
            del loginCheck
            i += 1

            if i == 10:
                return Response('error')
        try:
            User.objects.get(username=ID)

            return Response({'username': userName, 'overlap': 1})
        except User.DoesNotExist:
            return Response({'username': userName, 'overlap': 0})


class TestCheck(APIView):
    def post(self, request, format=None):
        # received_json_data = json.loads(request.body.decode("utf-8"))
        # ID = received_json_data['ID']
        # PW = received_json_data['PW']

        ID = request.POST['ID']
        PW = request.POST['PW']

        return Response((ID, PW))


class BookList(APIView):
    """
    코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
    """
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        books = UsedBook.objects.all()
        serializer = UsedBookSerializer(books, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UsedBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)

            return Response('Success', status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """

    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return UsedBook.objects.get(pk=pk)
        except UsedBook.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        permission = checkUser()

        return permission.permissionGet(UsedBookSerializer, snippet, self.request.user)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        permission = checkUser()

        return permission.permissionPut(UsedBookSerializer, snippet, request.data, self.request.user)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        permission = checkUser()

        if permission.permissionDelBuy(snippet, self.request.user):
            Request.objects.filter(bookId=pk).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        raise Http404


class MyBookList(APIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """

    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        user = self.request.user

        if snippet.username == str(user):
            snippet = user.books.all()
            serializer = UsedBookSerializer(snippet, many=True)

            return Response(serializer.data)

        raise Http404


class MyRequestList(APIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """

    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        user = self.request.user
        bookList = []
        requestList = []

        if snippet.username == str(user):
            snippet = user.requestbuyers.all()
            for snippetFilter in snippet:
                bookList.append((snippetFilter.pk, snippetFilter.bookId))
            for snippetFilter in bookList:
                try:
                    book = UsedBook.objects.get(pk=snippetFilter[1])


                    requestList.append({'author' : book.author, 'bookTitle' : book.bookTitle,
                                        'cource' : book.cource, 'id' : book.pk,
                                        'isbn' : book.isbn, 'owner' : str(book.owner),
                                        'professor' : book.professor, 'publisher' : book.publisher,
                                        'requestId' : snippetFilter[0]})
                except UsedBook.DoesNotExist:
                    raise Http404

            return Response(requestList)

        raise Http404


class SearchBook(APIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """

    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, bookName, format=None):
        search = UsedBook.objects.filter(bookTitle__icontains=bookName)
        serializer = UsedBookSerializer(search, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        bookName = request.POST['bookName']
        search = UsedBook.objects.filter(bookTitle__icontains=bookName)
        serializer = UsedBookSerializer(search, many=True)

        return Response(serializer.data)


class MyBuyBook(APIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """

    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, bookId, format=None):
        snippet = self.get_object(pk)
        user = self.request.user

        if snippet.username == str(user):
            snippet = Request.objects.filter(bookId=bookId)
            serializer = RequestSerializer(snippet, many=True)

            return Response(serializer.data)

        raise Http404


class BuyCheckBook(APIView):
    """
    코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
    """
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        books = Request.objects.all()
        serializer = RequestSerializer(books, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        user = self.request.user
        bookId = request.POST['bookId']
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                UsedBook.objects.get(pk=bookId)

                filterSet = user.books.all()
                if filterSet.filter(pk=bookId):
                    raise Http404

                filterSet = user.requestbuyers.all()
                if filterSet.filter(bookId=bookId):
                    raise Http404
            except UsedBook.DoesNotExist:
                raise Http404

            serializer.save(owner=self.request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCheckDetail(APIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """

    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        permission = checkUser()

        return permission.permissionDel(snippet, self.request.user)