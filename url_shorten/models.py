from django.db import models

class URLS(models.Model):
    date_created = models.DateTimeField('date published')
    original_url = models.CharField(max_length=65) # ¯\_(ツ)_/¯ Placeholder 65. Used b/c that was bit.ly's max
    shortened_slug = models.CharField(max_length=65)

# Equivalent to the following SQL
# Command can be found here https://docs.djangoproject.com/en/3.1/intro/tutorial02/#activating-models

# BEGIN;
# --
# -- Create model URLS
# --
# CREATE TABLE "url_shorten_urls" (
# "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, # Automatically set by Django
# "date_created" datetime NOT NULL,
# "original_url" varchar(65) NOT NULL,
# "shortened_url" varchar(65) NOT NULL,
# "http_code" varchar(3) NOT NULL);
# 
# COMMIT;