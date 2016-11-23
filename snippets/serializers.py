from rest_framework import serializers
from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, UsedBook, Request
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=UsedBook.objects.all())
    requestbuyers = serializers.PrimaryKeyRelatedField(many=True, queryset=Request.objects.all())
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'books', 'requestbuyers')


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    check_password = serializers.CharField(required=True)


class UsedBookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = UsedBook
        fields = ('id', 'bookTitle', 'author', 'publisher', 'isbn', 'cource', 'professor', 'owner')


class RequestSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Request
        fields = ('id', 'bookId', 'owner')