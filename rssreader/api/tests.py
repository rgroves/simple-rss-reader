import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from api.serializers import UserSerializer

# Create your tests here.
class UserRegisterTest(TestCase):
    # initialize the APIClient app
    client = Client()

    def test_user_register(self):
        """
        Test if user registration is successful (for happy path).
        """
        url = reverse('user_register')
        resp = self.client.post(url, {'username': 'test', 'password': 'myTe$tPw#'})
        token_length = Token._meta.get_field('key').max_length
        expected_content_regex = '{"access_token":"[0-9a-f]{' + str(token_length) + '}"}'
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertRegex(str_content, expected_content_regex)

    def test_user_register_must_provide_user(self):
        url = reverse('user_register')
        resp = self.client.post(url, {'username': '', 'password': 'te$ter#'})
        expected_content = {"username":["This field may not be blank."]}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_must_provide_password(self):
        url = reverse('user_register')
        resp = self.client.post(url, {'username': 'tester', 'password': ''})
        expected_content = {"password":["This field may not be blank."]}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_fail_on_duplicate_user(self):
        # Create user 'test'
        url = reverse('user_register')
        resp = self.client.post(url, {'username': 'test', 'password': 'myTe$tPw#'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Attempt to create a duplicate 'test' user
        url = reverse('user_register')
        resp = self.client.post(url, {'username': 'test', 'password': 'an0th3rPw#'})
        expected_content = {"username":["A user with that username already exists."]}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_get_not_allowed(self):
        url = reverse('user_register')
        resp = self.client.get(url)
        expected_content = {"detail": "Method \"GET\" not allowed."}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_head_not_allowed(self):
        url = reverse('user_register')
        resp = self.client.head(url)
        expected_content = ''
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(str_content, expected_content)

    def test_user_register_put_not_allowed(self):
        url = reverse('user_register')
        resp = self.client.put(url)
        expected_content = {"detail": "Method \"PUT\" not allowed."}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_delete_not_allowed(self):
        url = reverse('user_register')
        resp = self.client.delete(url)
        expected_content = {"detail": "Method \"DELETE\" not allowed."}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_trace_not_allowed(self):
        url = reverse('user_register')
        resp = self.client.trace(url)
        expected_content = {"detail": "Method \"TRACE\" not allowed."}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_patch_not_allowed(self):
        url = reverse('user_register')
        resp = self.client.patch(url)
        expected_content = {"detail": "Method \"PATCH\" not allowed."}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(str_content, json.dumps(expected_content))
