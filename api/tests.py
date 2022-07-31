from django.test import TestCase
from django.test import TestCase, Client
from music.models import Artist, Song, Album


class TestIndexView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.message = 'Hello world'
    def get_message(self):
        response = self.client.get('/api')
        data = response.data
        self.assertEqual(len(data), 10)

