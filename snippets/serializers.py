from rest_framework import serializers
from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, User, UsedBook, Request


class UserSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=UsedBook.objects.all())
    requestbuyers = serializers.PrimaryKeyRelatedField(many=True, queryset=Request.objects.all())
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            name = validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'name', 'books', 'requestbuyers')


# class ProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Profile
#         fields = ('name')


# class UserSerializer(serializers.ModelSerializer):
#     books = serializers.PrimaryKeyRelatedField(many=True, queryset=UsedBook.objects.all())
#     requestbuyers = serializers.PrimaryKeyRelatedField(many=True, queryset=Request.objects.all())
#     password = serializers.CharField(write_only=True)
#
#     profile = ProfileSerializer()
#
#     # def create(self, validated_data):
#     #     profile_data = validated_data.pop('profile', None)
#     #     user = super(UserSerializer, self).create(validated_data)
#     #     self.create_or_update_profile(user, profile_data)
#     #     return user
#
#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile', None)
#         user = User.objects.create(username=validated_data['username'], password=validated_data['password'])
#         Profile.objects.create(user=user, name=profile_data['name'])
#         return user
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password', 'books', 'requestbuyers', 'profile')


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