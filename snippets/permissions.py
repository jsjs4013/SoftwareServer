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
    """

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

    def permissionDelBuy(self, snippet, user):
        if snippet.owner == user:
            snippet.delete()

            return True

        raise False