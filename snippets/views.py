from snippets.models import User, UsedBook, Request, ChatList
from snippets.serializers import UserSerializer, UsedBookSerializer, RequestSerializer, ChatSerializer
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

from snippets.firebase import Firebase
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


class UserChange(UpdateAPIView):

    model = User
    queryset = User.objects.all()
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer


class ChatListGETPOST(APIView):
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
            snippet = snippet.chatLists.all()
            serializer = ChatSerializer(snippet, many=True)

            return Response(serializer.data)

        raise Http404

    def post(self, request, username, format=None):
        received_json_data = json.loads(request.body.decode("utf-8"))
        # received_json_data = request.data
        serializer = ChatSerializer(data=received_json_data)
        if serializer.is_valid():
            serializer.save(studentId=self.request.user)

            return Response('Success', status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatListDetail(APIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return ChatList.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, username, pk, format=None):
        received_json_data = json.loads(request.body.decode("utf-8"))
        snippet = self.get_object(pk)
        user = self.request.user
        # received_json_data = request.data

        permission = checkUser()

        return permission.permissionChatPut(ChatSerializer, snippet, received_json_data, self.request.user)


class LoginCommit(APIView):
    def post(self, request, format=None):
        received_json_data = json.loads(request.body.decode("utf-8"))
        ID = received_json_data['ID']
        PW = received_json_data['PW']

        loginCheck = EclassCheck()
        userName = loginCheck.check(ID, PW)
        del loginCheck

        if userName == False:
            loginCheck = EclassCheck()
            userName = loginCheck.check(ID, PW)
            del loginCheck

        if userName == False:
            return Response('error')
        try:
            User.objects.get(username=ID)

            return Response({'username': userName, 'overlap': 1})
        except User.DoesNotExist:
            return Response({'username': userName, 'overlap': 0})


class TestLoginCommit(APIView):
    def get(self, request, my_parameter, my_parameters, format=None):
        ID = my_parameter
        PW = my_parameters


        res = Firebase("dmkka0CerK4:APA91bGxCBLn2G9E8YmIqzkuCMvt0of7D1n2cE0rmbi2jp0U0pjdAdZ-XNapYr8zxofkml1n5jqztdLrNS83wJgiBO8bl-pzJGuL7N9cVTRl7CI3_BAKDv6YuV0wPjQG4IW8ZKa7Mk_K")
        return Response(res.push('제목', '바디'))

        loginCheck = EclassCheck()
        userName = loginCheck.check(ID, PW)
        del loginCheck

        if userName == False:
            loginCheck = EclassCheck()
            userName = loginCheck.check(ID, PW)
            del loginCheck

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

        if snippet.username == user.username:
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
                                        'comment' : book.comment, 'status' : book.status,
                                        'price' : book.price, 'sellerPrice' : book.sellerPrice,
                                        'pubdate' : book.pubdate, 'image' : book.image,
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

        if snippet.username == user.username:
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

    def get_bookInfo(self, pk):
        try:
            return UsedBook.objects.get(pk=pk)
        except UsedBook.DoesNotExist:
            raise Http404

    def get_UserInfo(self, username):
        try:
            return User.objects.get(pk=username)
        except User.DoesNotExist:
            raise Http404

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

            serializer = self.get_bookInfo(bookId)
            serializer = self.get_UserInfo(serializer.owner)

            return Response(serializer.token)

            pushMessage = Firebase()

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