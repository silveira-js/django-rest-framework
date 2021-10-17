from django.test import TestCase

from django.contrib.auth import get_user_model

User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='josucao', email='josucao@gmail.com')
        user.set_password('123456')
        user.save()
    
    def test_created_user(self):
        qs = User.objects.filter(username='josucao')
        self.assertEqual(qs.count(), 1)