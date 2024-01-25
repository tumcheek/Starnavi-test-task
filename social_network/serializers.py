from rest_framework import serializers

from .models import Post, User, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'created_at')
        extra_kwargs = {'created_at': {'read_only': True}}


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_login', 'last_request_date')


class AnalyticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ["user", "created_at", "post"]


class EmptyRequestBodySerializer(serializers.Serializer):
    pass
