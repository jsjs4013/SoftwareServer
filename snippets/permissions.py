"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 permission

 공통적으로 나타나는 클래스
 Meta class - 기본적인 반환형과 현재 serializer클래스가 사용하는 model을 설정한다.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import permissions, status


class checkUser(APIView):
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