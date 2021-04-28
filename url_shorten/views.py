from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

import random
import string
import datetime

from .forms import URL_Field
from .models import URLS

# def index(request):
#     return render(request, 'url_shortener/index.html')
def create_slug(length = 8):
    slug = random.choices(string.ascii_letters + string.digits, k = length)
    return "".join(slug)

def create_shorten_obj(request):
    url_form = URL_Field(request.POST)
    if url_form.is_valid():
        slug = create_slug()
        url = url_form.cleaned_data['url']
        new_url = URLS(date_created = datetime.datetime.now(), original_url = url, shortened_slug = slug, http_code = "TODO")
        new_url.save()
        return new_url

def shorten_and_pass_data(request):
    new_url = None
    form = None
    if request.method == "POST":
        create_shorten_obj(request)
        # url_form = URL_Field(request.POST)
        # if url_form.is_valid():
        #     slug = create_slug()
        #     url = url_form.cleaned_data['url']
        #     new_url = URLS(date_created = datetime.datetime.now(), original_url = url, shortened_slug = slug, http_code = "TODO")
        #     new_url.save()
        #     # request.user.url_shorten.add(new_url)
        return HttpResponseRedirect('/url_shorten')
    else:
        form = URL_Field()
    data = URLS.objects.all()
    context = {
        'form': form,
        'data': data,
        'short_url': new_url
    }
    return render(request, 'url_shortener/index.html', context)

def url_redirect(request, slugs):
    # TODO finds appropriate slug in db and returns redirect to original url
    data = URLS.objects.get(shortened_slug=slugs)
    return redirect(data.original_url)

    # data = UrlData.objects.get(slug=slugs)
    # return redirect(data.url)

    # slug - lkajdljk
    # original_url = google.com

def temp_url(request):
    # solely redirects to google.com
    return redirect("https://www.google.com")