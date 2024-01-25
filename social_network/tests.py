import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from freezegun import freeze_time

from .models import User, Post, Like
from .serializers import UserActivitySerializer


@pytest.fixture
def user_data():
    return {
        'username': 'user',
        'password': 'test_password123'
    }


@pytest.fixture
def test_user():
    return User.objects.create_user(username='TestUser')


@pytest.fixture
def test_post(post_data, test_user):
    return Post.objects.create(title=post_data['title'], body=post_data['body'], author=test_user)


@pytest.fixture
def post_data():
    return {
        'title': 'test',
        'body': 'test'
    }


@pytest.fixture
def user_create_url():
    return reverse('social_network:users')


@pytest.fixture
def post_url():
    return reverse('social_network:post-list')


@pytest.fixture
def post_detail_url(test_post):
    return reverse('social_network:post-detail', kwargs={'pk': test_post.pk})


@pytest.fixture
def post_like_url(test_post):
    return reverse('social_network:post-like', kwargs={'pk': test_post.pk})


@pytest.fixture
def post_unlike_url(test_post):
    return reverse('social_network:post-unlike', kwargs={'pk': test_post.pk})


@pytest.fixture
def user_activity_url():
    return reverse('social_network:user-activity')


@pytest.fixture
def analytics_url():
    return reverse('social_network:like-list')


@pytest.fixture
def authenticated_client(test_user):
    client = APIClient()
    client.force_authenticate(user=test_user)
    return client


@pytest.fixture
def like_responses():
    return {
        'status': 'liked',
        'error': 'You already liked this'
    }


@pytest.fixture
def unlike_responses():
    return {
        'status': 'unliked',
        'error': 'You already unliked this'
    }


@pytest.fixture
def liked_post(test_user, test_post):
    return Like.objects.create(user=test_user, post=test_post)


@pytest.fixture
def another_test_user():
    return User.objects.create_user(username='TestUser2')


@pytest.fixture
@freeze_time('2023-06-11')
def liked_post_with_another_user(another_test_user, test_post):
    return Like.objects.create(user=another_test_user, post=test_post)


@pytest.mark.django_db
class TestUserAPIView:

    def test_create_user(self, client, user_create_url, user_data):
        response = client.post(user_create_url, user_data)
        assert response.status_code == 201
        assert response.data['username'] == user_data['username']


@pytest.mark.django_db
class TestPostViewSet:
    def test_create_post(self, authenticated_client, post_url, post_data):
        response = authenticated_client.post(post_url, post_data)
        assert response.status_code == 201
        assert response.data['title'] == post_data['title']
        assert response.data['body'] == post_data['body']

    def test_get_posts(self, authenticated_client, post_url, test_post):
        response = authenticated_client.get(post_url)
        assert response.status_code == 200
        assert len(response.data['results']) == Post.objects.count()
        assert response.data['results'][0]['title'] == test_post.title
        assert response.data['results'][0]['body'] == test_post.body

    def test_get_post(self, authenticated_client, post_detail_url, test_post):
        response = authenticated_client.get(post_detail_url)
        assert response.status_code == 200
        assert response.data['title'] == test_post.title
        assert response.data['body'] == test_post.body

    def test_delete_method(self, authenticated_client, post_detail_url):
        response = authenticated_client.delete(post_detail_url)
        assert response.status_code == 204
        assert Post.objects.count() == 0

    def test_like_action(self, authenticated_client, post_like_url, like_responses):
        response = authenticated_client.post(post_like_url)
        assert response.data['status'] == like_responses['status']

    def test_unlike_action(self, authenticated_client, post_like_url, post_unlike_url, unlike_responses):
        authenticated_client.post(post_like_url)
        response = authenticated_client.post(post_unlike_url)
        assert response.data['status'] == unlike_responses['status']


@pytest.mark.django_db
class TestUserActivityAPIView:
    def test_get_user_activity(self, authenticated_client, user_activity_url, test_user):
        authenticated_client.get(user_activity_url)
        user_activity = UserActivitySerializer(test_user).data
        response = authenticated_client.get(user_activity_url)
        assert response.status_code == 200
        assert response.data == user_activity


@pytest.mark.django_db
class TestAnalyticsViewSet:
    def test_get_analytics(self, authenticated_client, analytics_url, liked_post, liked_post_with_another_user):
        query_params = {'date_from': '2024-01-09', 'date_to': '2024-09-02'}
        response = authenticated_client.get(analytics_url, data=query_params)
        assert response.status_code == 200
        assert len(response.data['results']) == 1


