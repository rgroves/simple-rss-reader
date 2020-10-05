import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from api.serializers import UserSerializer

class UserRegisterTest(TestCase):
    """
    Tests for user/register endpoint.
    """
    # initialize the APIClient app
    client = Client()
    endpoint = reverse('user_register')

    def test_user_register(self):
        """
        Test if user registration is successful (for happy path).
        """
        resp = self.client.post(self.endpoint, {'username': 'test', 'password': 'myTe$tPw#'})
        token_length = Token._meta.get_field('key').max_length
        expected_content_regex = '{"access_token":"[0-9a-f]{' + str(token_length) + '}"}'
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertRegex(str_content, expected_content_regex)

    def test_user_register_must_provide_user(self):
        """
        Test to ensure bad request if no user name value is provided in the post data.
        """
        resp = self.client.post(self.endpoint, {'username': '', 'password': 'te$ter#'})
        expected_content = {"username":["This field may not be blank."]}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_must_provide_password(self):
        """
        Test to ensure bad request if no password value is provided in the post data.
        """
        resp = self.client.post(self.endpoint, {'username': 'tester', 'password': ''})
        expected_content = {"password":["This field may not be blank."]}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_fail_on_duplicate_user(self):
        """
        Test to ensure bad request if a duplicate user name is provided in the post data.
        """
        # Create user 'test'
        resp = self.client.post(self.endpoint, {'username': 'test', 'password': 'myTe$tPw#'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Attempt to create a duplicate 'test' user
        resp = self.client.post(self.endpoint, {'username': 'test', 'password': 'an0th3rPw#'})
        expected_content = {"username":["A user with that username already exists."]}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_get_not_allowed(self):
        """
        Test to ensure that GET method is not allowed.
        """
        resp = self.client.get(self.endpoint)
        expected_content = {"detail": "Method \"GET\" not allowed."}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_head_not_allowed(self):
        """
        Test to ensure that HEAD method is not allowed.
        """
        resp = self.client.head(self.endpoint)
        expected_content = ''
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(str_content, expected_content)

    def test_user_register_put_not_allowed(self):
        """
        Test to ensure that PUT method is not allowed.
        """
        resp = self.client.put(self.endpoint)
        expected_content = {"detail": "Method \"PUT\" not allowed."}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_delete_not_allowed(self):
        """
        Test to ensure that DELETE method is not allowed.
        """
        resp = self.client.delete(self.endpoint)
        expected_content = {"detail": "Method \"DELETE\" not allowed."}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_trace_not_allowed(self):
        """
        Test to ensure that TRACE method is not allowed.
        """
        resp = self.client.trace(self.endpoint)
        expected_content = {"detail": "Method \"TRACE\" not allowed."}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(str_content, json.dumps(expected_content))

    def test_user_register_patch_not_allowed(self):
        """
        Test to ensure that PATCH method is not allowed.
        """
        resp = self.client.patch(self.endpoint)
        expected_content = {"detail": "Method \"PATCH\" not allowed."}
        str_content = str(resp.content, encoding='utf8')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(str_content, json.dumps(expected_content))
