from django.test import TestCase
from .models import Status

from django.contrib.auth import get_user_model

User = get_user_model()

class StatusTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='josucao', email='josucao@gmail.com')
        user.set_password('123456')
        user.save()
    
    def test_creating_status(self):
        user = User.objects.get(username='josucao')
        obj = Status.objects.create(user=user, content='Some cool new content')
        self.assertEqual(obj.id, 1)
        qs = Status.objects.all()
        self.assertEqual(qs.count(), 1)