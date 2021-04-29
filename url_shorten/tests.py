from django.test import RequestFactory, TestCase, Client
from django.core.validators import URLValidator
from urllib.parse import urlparse

import time
import datetime

from .models import URLS
from .views import create_shorten_obj, create_slug, shorten_and_pass_data
from .forms import URL_Field

# TODO tests shouldn't require network connections. Look up Django mocked network requests
# tests for the first url in url_bank to return a 200. URL bank was picked based on various cloud hosting services in case one fails
url_bank = ["www.google.com", "www.microsoft.com", "www.amazon.com", "www.ovh.com", "www.alibaba.com"]
working_url = ""

for url in url_bank:
    response = Client().get(url)
    if response.status_code == 200:
        working_url = url
        break

class URLShortenerUnitTests(TestCase):

    def test_create_slug(self):
        """
        Tests slug creation
        """
        self.assertTrue(len(create_slug()) > 1)

    def test_slug_not_in_db(self): # TODO
        """
        Tests to see if slug correctly checks that it's not in db
        """
        self.assertRaises(URLS.DoesNotExist, URLS.objects.get, shortened_slug="FAILTEST")


    def test_slug_in_db(self): # TODO
        """
        Tests to see if slug correctly checks when slug already in db
        """
        slug = "TESTTEST"
        test_entry = URLS(date_created = datetime.datetime.now(), original_url = url, shortened_slug = slug, http_code = "TODO")
        test_entry.save()
        self.assertTrue(URLS.objects.get(shortened_slug=slug))


    def test_POST_url_form(self):
        """
        Tests to see that request POSTed properly to url shortener form + validates URL
        """
        request = RequestFactory().post('/', { 'url': 'www.google.com'})
        form = URL_Field(request.POST)
        self.assertTrue(form.is_valid())

        request = RequestFactory().post('/', { 'NOT_A_PARAM': 'www.google.com'})
        form = URL_Field(request.POST)
        self.assertFalse(form.is_valid())

        request = RequestFactory().post('/', { 'url': 'www.INVALID_URL'})
        form = URL_Field(request.POST)
        self.assertFalse(form.is_valid())

    def test_shorten(self):
        """
        Tests that shorten() creates a valid object
        """
        request = RequestFactory().post('/', { 'url': 'http://www.google.com'})
        urls_obj = create_shorten_obj(request)
        print("urls_obj", urls_obj)
        self.assertNotEqual(urls_obj.date_created, None) # TODO Look up library to freeze cpu time
        self.assertEqual(urls_obj.original_url, 'http://www.google.com')
        self.assertEqual(len(urls_obj.shortened_slug), 8) # TODO 8 shouldn't be hardcoded
        # self.assertEqual(urls_obj.http_code, ) # TODO not sustainable

    def test_url_redirect(self):
        """
        Ensure that new instance of URL table was created
        """
        request = RequestFactory().post('/', { 'url': 'http://www.google.com'})
        urls_obj = shorten_and_pass_data(request)
        self.assertEqual(urls_obj.status_code, 302)

    def test_was_db_entry_created(self):
        """
        Was a db entry created after user shortens URL?
        """
        pass

    def test_simulated_server_down(self):
        """
        Frontend should tell user if response takes longer than 2 seconds. 500 error
        """
        pass
        # class DelayedShortener(URLS): # TODO this is wrong? Waits 5 seconds then activates?
        #     def delayed_shorten(self, url):
        #         time.sleep(5)
        #         return shorten(url)

        # test_url = DelayedShortener().delayed_shorten("www.google.com")        
        # self.assertEqual(Client().get(test_url).status_code, 500)

class URLShortenerIntegrationTests(TestCase):
    
    def test_shortened_url_works(self):
        """
        Does output URL work?
        """
        request = RequestFactory().post('/', { 'url': 'http://www.google.com'})
        urls_obj = create_shorten_obj(request)
        mock_resp = Client().get('/url_shorten/{}'.format(urls_obj.shortened_slug))
        self.assertEqual(mock_resp.status_code, 302)
        self.assertEqual(mock_resp.url, 'http://www.google.com')

    def test_bad_output(self):
        """
        Does shortened URL break if given bad output?
        Site doesn't exist - jlaksfjlksafjklasf.com
        
        """
        pass
        # test_url = shorten("non_working_url")
        # redirected_url = Client().get(test_url) # TODO Unsure if this is how you'd get the redirected url's status code
        # self.assertEqual(Client().get(redirected_url).status_code, 400) 
