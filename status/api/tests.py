import os
import tempfile
import shutil
from PIL import Image

import rest_framework
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from django.conf import settings
from rest_framework_jwt.settings import api_settings

from django.contrib.auth import get_user_model
from status.models import Status
User = get_user_model()

jwt_payload_handler            = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler             = api_settings.JWT_ENCODE_HANDLER

class StatusAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='testjosucao', email='josucao@gmail.com')
        user.set_password('123456')
        user.save()

        status_obj = Status.objects.create(user=user, content="Hello there")

    def test_statuses(self):
        qs = Status.objects.all()
        self.assertEqual(qs.count(), 1)

    def status_user_token(self):
        auth_url = api_reverse('api-auth:login')
        auth_data = {
            'username': 'testjosucao',
            'password': '123456',
        }
        auth_response = self.client.post(auth_url, auth_data, format='json')
        token = auth_response.data.get('token', 0)
        if token is not None:
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def create_item(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        data = {
            'content':'some cool testing content'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 2)
        return response.data

    def test_empty_create_item(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        data = {
            'content': None,
            'image': None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        return response.data

    def test_status_create_with_image(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        image_item = Image.new('RGB', (800, 1280), (0, 124, 174))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image_item.save(tmp_file, format='JPEG')
        print(tmp_file.name)
        with open(tmp_file.name, 'rb') as file_obj:
            data = {
                'content':'some cool testing content',
                'image': file_obj
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Status.objects.count(), 2)
            img_data = response.data.get('image')
            self.assertNotEqual(img_data, None)
        tmp_img_dir = os.path.join(settings.MEDIA_ROOT, 'status', 'testjosucao')
        if os.path.exists(tmp_img_dir):
            shutil.rmtree(tmp_img_dir)
        
    def test_status_create_with_image_no_content(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        image_item = Image.new('RGB', (800, 1280), (0, 124, 174))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image_item.save(tmp_file, format='JPEG')
        print(tmp_file.name)
        with open(tmp_file.name, 'rb') as file_obj:
            data = {
                'content': '',
                'image': file_obj
            }
            response = self.client.post(url, data, format='multipart')
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Status.objects.count(), 2)
        tmp_img_dir = os.path.join(settings.MEDIA_ROOT, 'status', 'testjosucao')
        if os.path.exists(tmp_img_dir):
            shutil.rmtree(tmp_img_dir)
        


    def test_status_create(self):
        data = self.create_item()
        data_id = data.get('id')
        rud_url = api_reverse('api-status:detail', kwargs={'id':data_id})
        rud_data = {
            'content':'another new cool testing content'
        }
        '''
        get / retrieve
        '''
        get_response = self.client.get(rud_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_status_update(self):
        data = self.create_item()
        data_id = data.get('id')
        rud_url = api_reverse('api-status:detail', kwargs={'id':data_id})
        rud_data = {
            'content':'another new cool testing content'
        }
       
        '''
        put / update
        '''
        put_response = self.client.put(rud_url, rud_data, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        put_response_data = put_response.data
        self.assertEqual(put_response_data['content'], rud_data['content'])
    
    def test_status_delete(self):
        data = self.create_item()
        data_id = data.get('id')
        rud_url = api_reverse('api-status:detail', kwargs={'id':data_id})

        '''
        delete
        '''
        del_response = self.client.delete(rud_url, format='json')
        self.assertEqual(del_response.status_code, status.HTTP_204_NO_CONTENT)

        '''
        Not found
        '''
        get_response = self.client.get(rud_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_status_not_token_create(self):
        url = api_reverse('api-status:list')
        data = {
            'content':'some cool testing content'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_other_user_permissions(self):
        data        = self.create_item()
        data_id     = data.get('id')
        user        = User.objects.create(username='josuta')
        payload     = jwt_payload_handler(user)
        token       = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        rud_url     = api_reverse('api-status:detail', kwargs={'id':data_id})
        rud_data    = {
                        'content':'smashing'
                    }
        get_        = self.client.get(rud_url, format='json')
        put_        = self.client.put(rud_url, rud_data, format='json')
        delete_     = self.client.delete(rud_url, format='json')
        self.assertEqual(get_.status_code, status.HTTP_200_OK)
        self.assertEqual(put_.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_.status_code, status.HTTP_403_FORBIDDEN)
