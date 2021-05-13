# External libraries
from django.test import RequestFactory, TestCase, Client
from django.core.validators import URLValidator
from urllib.parse import urlparse
from freezegun import freeze_time

# Default libraries
import time
import datetime
import inspect

# Internal files
from .models import URLS
from .views import create_shorten_obj, create_slug, shorten_and_pass_data
from .forms import URL_Field

class URLShortenerUnitTests(TestCase):

    def test_create_slug(self):
        """
        Tests slug creation
        """
        self.assertTrue(len(create_slug()) > 1)

    def test_slug_not_in_db(self):
        """
        Tests to see if slug correctly checks that it's not in db
        """
        self.assertRaises(URLS.DoesNotExist, URLS.objects.get, shortened_slug="FAILTEST")

    def test_slug_in_db(self):
        """
        Tests to see if slug correctly checks when slug already in db
        """
        slug = "PASSTEST"
        url = "www.google.com"
        test_entry = URLS(date_created = datetime.datetime.now(), original_url = url, shortened_slug = slug)
        test_entry.save()
        self.assertEqual(URLS.objects.get(shortened_slug=slug), test_entry)

    def test_POST_url_form(self):
        """
        Tests to see that request POSTed properly to url shortener form + validates URL
        """
        request = RequestFactory().post('/', { 'url': 'www.google.com'})
        form = URL_Field(request.POST)
        self.assertTrue(form.is_valid())

    def test_POST_url_form_bad_key(self):
        """
        Request should not be valid because wrong param is used
        """
        request = RequestFactory().post('/', { 'NOT_A_PARAM': 'www.google.com'})
        form = URL_Field(request.POST)
        self.assertFalse(form.is_valid())

    def test_POST_url_form_bad_value(self):
        """
        Request should not be valid because URL is invalid
        """
        request = RequestFactory().post('/', { 'url': 'www.INVALID_URL'})
        form = URL_Field(request.POST)
        self.assertFalse(form.is_valid())

    @freeze_time("2021-05-12")
    def test_shorten(self):
        """
        Tests that shorten() creates a valid object
        """
        request = RequestFactory().post('/', { 'url': 'http://www.google.com'})
        urls_obj = create_shorten_obj(request)
        default_slug_len = inspect.getargspec(create_slug).defaults[0] # NOTE getargspec used to get default parameters to function

        self.assertEqual(urls_obj.date_created, datetime.datetime.now()) # NOTE datetime is mocked w/ freezegun
        self.assertEqual(urls_obj.original_url, 'http://www.google.com')
        self.assertEqual(len(urls_obj.shortened_slug), default_slug_len) 

    def test_was_db_entry_created(self):
        """
        Was a db entry created after user shortens URL?
        """
        current_db_size = len(URLS.objects.all())
        slug = "PASSTEST"
        url = "www.google.com"
        test_entry = URLS(date_created = datetime.datetime.now(), original_url = url, shortened_slug = slug)
        test_entry.save()
        self.assertEqual(len(URLS.objects.all()), current_db_size + 1)

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

    def test_bad_input(self):
        """
        Shortened URL should allow for bad input and still shorten
        - Site doesn't exist
        - improperly formatted url
        """
        request = RequestFactory().post('/', { 'url': 'http://www.jlaksfjlksafjklasf.com'})
        urls_obj = create_shorten_obj(request)
        mock_resp = Client().get('/url_shorten/{}'.format(urls_obj.shortened_slug))
        self.assertEqual(mock_resp.status_code, 302)
        self.assertEqual(mock_resp.url, 'http://www.jlaksfjlksafjklasf.com')

        request = RequestFactory().post('/', { 'url': 'httpwjlaksfjlksafjklasf.com'})
        urls_obj = create_shorten_obj(request)
        mock_resp = Client().get('/url_shorten/{}'.format(urls_obj.shortened_slug))
        self.assertEqual(mock_resp.url, 'http://httpwjlaksfjlksafjklasf.com')
        self.assertEqual(mock_resp.status_code, 302)

    def test_url_redirect(self):
        """
        Ensure that new instance of URL table was created
        """
        request = RequestFactory().post('/', { 'url': 'http://www.google.com'})
        urls_obj = shorten_and_pass_data(request)
        self.assertEqual(urls_obj.status_code, 302)