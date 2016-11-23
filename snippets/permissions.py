from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import permissions, status


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        객체의 소유자에게만 쓰기를 허용하는 커스텀 권한
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용하므로,
        # GET, HEAD, OPTIONS 요청은 항상 허용함
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 코드 조각의 소유자에게만 부여함
        return obj.owner == request.user


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