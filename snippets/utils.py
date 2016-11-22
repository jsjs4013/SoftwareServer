# from rest_framework import serializers
#
# from rest_framework_jwt.serializers import JSONWebTokenSerializer
# from rest_framework_jwt.compat import Serializer, PasswordField
#
# from rest_framework_jwt.views import ObtainJSONWebToken
#
#
# class JSONWebTokenCustomSerializer(JSONWebTokenSerializer):
#     def __init__(self, *args, **kwargs):
#         """
#         Dynamically add the USERNAME_FIELD to self.fields.
#         """
#         super(JSONWebTokenCustomSerializer, self).__init__(*args, **kwargs)
#
#         self.fields[self.username_field] = serializers.CharField()
#         self.fields['password'] = PasswordField(write_only=True)
#
#
# class ObtainCustomJSONWebToken(ObtainJSONWebToken):
#     serializer_class = JSONWebTokenCustomSerializer
#
# obtain_jwt_token_custom = ObtainCustomJSONWebToken.as_view()


from snippets.serializers import SnippetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status


class checkUser(APIView):
    def permissionGet(self, snippet, user):
        if snippet.owner == user:
            serializer = SnippetSerializer(snippet)
            return Response(serializer.data)
        raise Http404

    def permissionPut(self, snippet, data, user):
        if snippet.owner == user:
            serializer = SnippetSerializer(snippet, data=data)
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