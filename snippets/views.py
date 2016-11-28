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

import requests
from bs4 import BeautifulSoup

class TestLoginCommit(APIView):
    def get(self, request, my_parameter, my_parameters, format=None):
        ID = my_parameter
        PW = my_parameters

        # loginCheck = EclassCheck()
        # userName = loginCheck.check(ID, PW)
        # del loginCheck
        i = 0

        login_info = {
            'userDTO.userId': ID,  # YourID 2014112025
            'userDTO.password': PW  # YourPW wlsduddl14!
        }

        # 실제 로그인 하는 부분. Dict 형태로 로그인 정보를 담아 request 보냄. Request 생성 시 두번째 인자가 들어오게 되면 자동으로 Post Request로 인식
        login_url = 'https://eclass.dongguk.edu/User.do?cmd=loginUser'  # 로그인 검증 페이지
        session = requests.session()
        r = session.post(login_url, data=login_info)

        #### LOGIN CHECK ####
        main_url = 'https://eclass.dongguk.edu/Main.do?cmd=viewEclassMain&mainMenuId=menu_00050&subMenuId=&menuType=menu'
        r = session.get(main_url, timeout=5)
        data = r.content.decode('utf-8')
        soup = BeautifulSoup(data, "html.parser")

        try:  # 로그인 실패시 예외처리
            userName = soup.find('span', {'class': 'user'}).find('strong').text
            userName = userName.strip()  # 양쪽 끝의 공백 문자 제거
            session.close()

            try:
                User.objects.get(username=ID)

                return Response({'username': userName, 'overlap': 1})
            except User.DoesNotExist:
                return Response({'username': userName, 'overlap': 0})
        except  AttributeError:
            return Response('error')

        # while userName == False:
        #     loginCheck = EclassCheck()
        #     userName = loginCheck.check(ID, PW)
        #     del loginCheck
        #     i += 1
        #
        #     if i == 5:
        #         return Response('error')
        if userName == False:
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
        received_json_data = json.loads(request.body.decode("utf-8"))
        serializer = UsedBookSerializer(data=received_json_data)
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
        received_json_data = json.loads(request.body.decode("utf-8"))
        snippet = self.get_object(pk)
        permission = checkUser()

        return permission.permissionPut(UsedBookSerializer, snippet, received_json_data, self.request.user)

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

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        snippet = self.get_object(username)
        user = self.request.user

        if snippet.username == user.username:
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

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        snippet = self.get_object(username)
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
                                        'isbn' : book.isbn, 'owner' : book.owner.username,
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
        received_json_data = json.loads(request.body.decode("utf-8"))
        bookName = received_json_data['bookName']
        # bookName = request.POST['bookName']
        search = UsedBook.objects.filter(bookTitle__icontains=bookName)
        serializer = UsedBookSerializer(search, many=True)

        return Response(serializer.data)


class MyBuyBook(APIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """

    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, bookId, format=None):
        snippet = self.get_object(username)
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
        received_json_data = json.loads(request.body.decode("utf-8"))
        bookId = received_json_data['bookId']
        # bookId = request.POST['bookId']
        user = self.request.user
        serializer = RequestSerializer(data=received_json_data)
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