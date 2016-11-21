from rest_framework import serializers

from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.compat import Serializer, PasswordField

from rest_framework_jwt.views import ObtainJSONWebToken


class JSONWebTokenCustomSerializer(JSONWebTokenSerializer):
    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(JSONWebTokenCustomSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)


class ObtainCustomJSONWebToken(ObtainJSONWebToken):
    serializer_class = JSONWebTokenCustomSerializer

obtain_jwt_token_custom = ObtainCustomJSONWebToken.as_view()