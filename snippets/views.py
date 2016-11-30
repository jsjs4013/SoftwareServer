"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 django rest framework에서 view에 해당하는 파일이다.
 대부분의 MVC패턴에서 V와 몇몇의 C를 담당하는 파일이다.

 클래스들에 공통으로 나타나는 파라미터 및 메서드들을 정리한다.
 queryset - 모델의 정보를 받아오는 파라미터
 serializer_class - 모델과 view를 이어주는 serializer의 정보를 받아오는 파라미터
 authentication_classes - 무엇으로 토큰 인증을 받을지를 결정한다.
 permission_classes - 만약 인증이 된다면 서버에 접근권한을 설정해준다.
 get - GET요청을 처리한다.
 post - POST요청을 처리한다.
 put - PUT요청을 처리한다.
 delete - DELETE요청을 처리한다.
"""

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
    """
     회원가입한 유저들의 리스트를 보여주는 클래스이다.
     GET방식으로 요청을 받아 처리한다.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
     회원가입한 유저들의 pk를 URI로 받아와 그 유저의 세세한 정보를 보여주는 클래스이다.
     GET방식으로 요청을 받아 처리한다.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserManage(CreateAPIView):
    """
     처음 회원가입할 때 유저를 데이터베이스에 생성시켜주는 클래스이다.
     POST방식으로 요청을 받아 처리한다.
    """
    model = User
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class UserChange(UpdateAPIView):
    """
     푸시메시지를 위한 유저의 토큰을 변경시키기 위해 존재하는 클래스이다.
     PUT방식으로 요청을 받아 처리한다.
    """
    model = User
    queryset = User.objects.all()
    lookup_field = 'username'
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer


# class UserChange(APIView):
#     """
#      푸시메시지를 위한 유저의 토큰을 변경시키기 위해 존재하는 클래스이다.
#      PUT 방식으로 요청을 받아 처리한다.
#     """
#     authentication_classes = (authentication.JSONWebTokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get_object(self, username):
#         try:
#             return User.objects.get(username=username)
#         except User.DoesNotExist:
#             raise Http404
#
#     def put(self, request, username, format=None):
#         received_json_data = json.loads(request.body.decode("utf-8"))
#         # received_json_data = request.data
#         snippet = self.get_object(username)
#
#         serializer = UserSerializer(snippet, data=received_json_data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response('Success')
#
#         raise Http404


class ChatListGETPOST(APIView):
    """
     URI를 요청할 때 주소에 포함된 학번을 체크하여 그 학번에 해당하는 채팅정보를 얻어오거나 생성한다.
     GET과 POST방식을 지원한다.
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
    """
     URI를 요청할 때 주소에 포함된 채팅정보의 pk를 체크하여 마지막 메시지를 갱신한다.
     PUT방식으로 요청을 받아 처리한다.
    """
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
    """
     학교홈페이지와 연동하여 로그인한 사용자의 상태를 체크하는 클래스이다.
     만약 학교와 관계된 사람이 아니라면 로그인 및 회원가입이 되지 않는다.
    """
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
    """
     테스트용 클래스
    """
    def get(self, request, my_parameter, my_parameters, format=None):
        ID = my_parameter
        PW = my_parameters


        # res = Firebase("dmkka0CerK4:APA91bGxCBLn2G9E8YmIqzkuCMvt0of7D1n2cE0rmbi2jp0U0pjdAdZ-XNapYr8zxofkml1n5jqztdLrNS83wJgiBO8bl-pzJGuL7N9cVTRl7CI3_BAKDv6YuV0wPjQG4IW8ZKa7Mk_K")
        # return Response(res.push(ID, PW, 'ㅇㄴㅁ'))

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
    """
     테스트용 클래스
    """
    def post(self, request, format=None):
        # received_json_data = json.loads(request.body.decode("utf-8"))
        # ID = received_json_data['ID']
        # PW = received_json_data['PW']

        ID = request.POST['ID']
        PW = request.POST['PW']

        return Response((ID, PW))


class BookList(APIView):
    """
     서버에 등록된 책을 모두 보여주거나 새로운 책을 등록한다.
     GET방식으로 등록된 책을 모두 보여준다.
     POST방식으로 새로운 책을 등록할 수 있다.
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
     URI에 포함된 등록한 책의 pk를 얻어와 그 책에 대한 세부조종을 하는 클래스이다.
     GET방식으로 해당되는 책 하나에 대한 정보를 얻어온다.
     PUT방식으로 해당되는 책의 정보를 업데이트 한다.
     DELETE방식으로 해당되는 책의 정보를 삭제한다.
     책이 삭제될 때 책과 연관되어있는 책 구매 요청 정보도 같이 삭제된다.
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
     유저가 등록한 책을 보여주는 클래스이다.
     URI로 유저의 학번을 받아와 그 학번에 해당되는 책 등록 리스트를 반환해준다.
     GET방식으로 요청을 받아 처리한다.
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
     내가 요청한 책의 리스트를 보여준다.
     URI에 포함된 학번을 체크하여 그 학번에 관계된 유저의 구매 요청 리스트를 적절한 형식으로 포매팅하여 반환하여준다.
     GET방식으로 요청을 받아 처리한다.
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
     책의 제목을 검색하여 그 검색된 책 정보를 반환하는 클래스이다.
     책의 검색은 POST를 통해 검색된다.
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
     내가 등록한 책을 구매 요청한 유저의 정보를 반환하는 클래스이다.
     URI에 포함된 학번을 현재 유저의 정보를 받아온 토큰값과 비교하여 유저임을 확인한 후 등록한 책을 구매 요청한 유저의 정보를 반환한다.
     GET방식으로 요청을 받아 처리한다.
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
     등록되어있는 책을 구매요청하는 클래스이다.
     GET방식으로 요청을하면 등록한 책에 대해서 모든 구매 요청 리스트를 보여준다.
     POST방식으로 요청을하면 해당되는 책에 대해서 구매요청을 할 수 있다.
     Google의 firebase cloud message를 사용하여 등록된 책이 구매요청되면 책을 등록한 사람에게 요청한 사람의 정보와 책의 제목을 푸시메시지로 보내준다.
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
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        books = Request.objects.all()
        serializer = RequestSerializer(books, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        received_json_data = json.loads(request.body.decode("utf-8"))
        bookId = received_json_data['bookId']
        # received_json_data = request.data
        # bookId = request.POST['bookId']
        user = self.request.user
        serializer = RequestSerializer(data=received_json_data)

        # 책을 중복신청하면 안되기에 처리하는 부분
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

            bookInfo = self.get_bookInfo(bookId)
            userInfo = self.get_UserInfo(bookInfo.owner)

            # firebase요청 부분
            pushMessage = Firebase(userInfo.token)
            pushMessage.push('구매요청', user.username, bookInfo.bookTitle)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCheckDetail(APIView):
    """
     사용자가 구매 요청한 책을 구매 요청 취소할 수 있는 클래스이다.
     URI에 포함된 구매요청 pk를 비교하여 그 pk에 해당되는 유저와 현재 로그인한 유저가 같은 사람이라면 구매요청을 취소한다.
     DELETE방식으로 요청을 한다.
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