"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 django rest framework에서 model과 view사이의 연결통로 및 적절한 컨트롤러 역할을 한다.
 외래키의처리 데이터형식설정 create, update등 model과 view의 사이에서 적절한 다리역할을 한다.

 공통적으로 나타나는 클래스
 Meta class - 기본적인 반환형과 현재 serializer클래스가 사용하는 model을 설정한다.
"""

from rest_framework import serializers
from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, User, UsedBook, Request, ChatList


class UserSerializer(serializers.ModelSerializer):
    """
     User model을 처리하는 serializer클래스이다.
     User model이 가지고있는 자식들을 확인하기 위해 PrimaryKeyRelatedField사용한다.
     자식들의 pk값이 User model에 등록된다.

     메서드
     create 회원가입을 위해 데이터베이스에 적절한 값을 생성해주는 메서드이다.
     update 푸시메시지를 위한 토큰업데이트를 위해 데이터베이스에 해당되는 유저에대한 토큰 값을 update하는 메서드이다.
    """
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=UsedBook.objects.all(), required=False)
    requestbuyers = serializers.PrimaryKeyRelatedField(many=True, queryset=Request.objects.all(), required=False)
    chatLists = serializers.PrimaryKeyRelatedField(many=True, queryset=ChatList.objects.all(), required=False)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username = validated_data['username'],
            name = validated_data['name'],
            token = validated_data['token']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.token = validated_data.get('token', instance.token)
        # instance.token = validated_data['token']
        instance.save()

        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'name', 'token', 'books', 'requestbuyers', 'chatLists')


class ChatSerializer(serializers.ModelSerializer):
    """
     ChatList model을 처리하는 serializer클래스이다.
     ChatList model이 가지고있는 외래키를 username만을 보여주도록 한다.

     변수
     studentId - 외래키를 사용하여 연결된 model의 username을 보여준다.
    """
    studentId = serializers.ReadOnlyField(source='studentId.username')

    class Meta:
        model = ChatList
        fields = ('id', 'studentId', 'partner', 'partnerName', 'lastMessage')


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
     유저의 비밀번호를 변경하기 위한 serializer클래스이다.
    """
    check_password = serializers.CharField(required=True)


class UsedBookSerializer(serializers.ModelSerializer):
    """
        ChatList model을 처리하는 serializer클래스이다.
        ChatList model이 가지고있는 외래키를 username만을 보여주도록 한다.

        변수
        studentId - 외래키를 사용하여 연결된 model의 username을 보여준다.
       """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = UsedBook
        fields = ('id', 'bookTitle', 'author', 'publisher', 'isbn', 'cource', 'professor', 'comment', 'status',
                  'sellerPrice', 'price', 'pubdate', 'image', 'owner')


class RequestSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Request
        fields = ('id', 'bookId', 'owner', 'ownerName')