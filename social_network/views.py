from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import models
from . import serializers
from .filters import AnalyticsFilter
from .mixins import LikeModelMixin


class UserAPIView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]


class PostViewSet(viewsets.ModelViewSet, LikeModelMixin):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnalyticsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Like.objects.all()
    serializer_class = serializers.AnalyticsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnalyticsFilter


class UserActivityAPIView(APIView):
    def get(self, request):
        serializer = serializers.UserActivitySerializer(request.user)
        return Response(serializer.data)
