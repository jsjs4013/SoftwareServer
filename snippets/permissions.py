"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 JWT만으로 권한을 설정하지 못할 때 사용하는 권한설정관련 파일이다.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import permissions, status


class checkUser(APIView):
    """
     권한을 설정해주고 GET, POST, PUT 그리고 DELETE를 적절하게 처리해주는 클래스이다.
     받아온 토큰인 JWT와 받아온 username이 적절한 권한을 줄 수 있는지 처리해준다.
    """

    # 아래 두개의 메서드는 책에대한 자세한 정보를 얻거나 책을 등록시키는 권한관리 메서드이다.
    def permissionGet(self, Serializer, snippet, user):
        if snippet.owner == user:
            serializer = Serializer(snippet)

            return Response(serializer.data)

        raise Http404

    def permissionPut(self, Serializer, snippet, data, user):
        if snippet.owner == user:
            serializer = Serializer(snippet, data=data)
            if serializer.is_valid():
                serializer.save()

                return Response('Success')

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        raise Http404

    # 채팅의 마지막 메시지를 갱신해주기 위해 필요한 권한관리 메서드이다.
    def permissionChatPut(self, Serializer, snippet, data, user):
        if snippet.studentId == user:
            serializer = Serializer(snippet, data=data)
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        raise Http404

    def permissionDel(self, snippet, user):
        if snippet.owner == user:
            snippet.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        raise Http404

    # 이 부분은 산 책 목록을 지우는 부분으로 True, False를 리턴해주어야하므로 Del을 하나 더 설정하였다.
    # 특수한 Del 메서드이다.
    def permissionDelBuy(self, snippet, user):
        if snippet.owner == user:
            snippet.delete()

            return True

        raise False