from django.test import  TestCase
from django.urls import reverse, resolve

from ..models import  Board,Topic,Post
from django.contrib.auth.models import User

from ..views import topic_detail


class TopicPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django', description='Django board.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        topic = Topic.objects.create(subject='Hello, world', board=board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user)
        url = reverse('board:topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/board/1/topic/1/')
        self.assertEquals(view.func, topic_detail)

    # def test_wrong_topic_id(self):
    #     url=rev
    #     self.assertEquals(self.response)