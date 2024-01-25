from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from drf_yasg import openapi

from .models import Like
from .serializers import EmptyRequestBodySerializer


class LikeModelMixin:
    @swagger_auto_schema(
        operation_description="Like a post",
        responses={
            200: openapi.Response("Successfully liked the post", openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description="liked")})),
            422: openapi.Response("Already liked", openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description="You already liked this")}))
        },
        request_body=EmptyRequestBodySerializer(),
        tags=['likes'],
    )
    @action(detail=True, methods=['post'])
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        try:
            Like.objects.create(user=request.user, post=post)
            return Response({'status': 'liked'})
        except IntegrityError:
            return Response({'error': 'You already liked this'}, status=422)

    @swagger_auto_schema(
        operation_description="Like a post",
        responses={
            200: openapi.Response("Successfully unliked the post", openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description="liked")})),
            422: openapi.Response("Already unliked this", openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description="You already liked this")}))
        },
        request_body=EmptyRequestBodySerializer(),
        tags=['likes'],
    )
    @action(detail=True, methods=['post'])
    def unlike(self, request, *args, **kwargs):
        post = self.get_object()
        try:
            Like.objects.get(user=request.user, post=post.pk).delete()
            return Response({'status': 'unliked'})
        except ObjectDoesNotExist:
            return Response({'error': 'You already unliked this'}, status=422)