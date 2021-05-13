from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.defaults import server_error

import random
import string
import datetime

from .forms import URL_Field
from .models import URLS

def create_slug(length = 8):
    slug = random.choices(string.ascii_letters + string.digits, k = length)
    return "".join(slug)

def create_shorten_obj(request):
    url_form = URL_Field(request.POST)
    if url_form.is_valid():
        slug = create_slug()
        url = url_form.cleaned_data['url']
        new_url = URLS(date_created = datetime.datetime.now(), original_url = url, shortened_slug = slug)
        new_url.save()
        return new_url

def shorten_and_pass_data(request):
    current_time = datetime.datetime.now()
    while (datetime.datetime.now() - current_time).total_seconds() < 2: # checks if queries are taking longer than 2s
        if request.method == "POST":
            create_shorten_obj(request)
            return HttpResponseRedirect('/url_shorten')
        else:
            form = URL_Field()
        data = URLS.objects.all()
        new_slug = URLS.objects.latest('date_created')
        context = {
            'form': form,
            'data': data,
            'new_slug': new_slug
        }
        return render(request, 'url_shortener/index.html', context)
    else:
        return server_error(request)

def url_redirect(request, slugs):
    data = URLS.objects.get(shortened_slug=slugs)
    return redirect(data.original_url)