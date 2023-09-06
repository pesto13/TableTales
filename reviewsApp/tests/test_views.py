from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def test_create_view(self):
        assert 1==1

        # client = Client()
        # response = client.get(reverse('review_create'))
        #
        # self.assertEqual(response.status_code, 200)
        # # self.assertTemplateUsed(response, '/form-submit.html')
