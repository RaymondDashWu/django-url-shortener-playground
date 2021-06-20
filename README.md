# Django URL Shortener

Simple URL shortener using many Django libraries. This project was created more with the intention of learning various TDD philosophies and practices with my mentor Richie Thomas (senior software engineer at Mavenlink)

## Getting Started

Setup project environment with [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io).

```bash
$ virtualenv project-env
$ source project-env/bin/activate
$ pip install -r https://github.com/RaymondDashWu/django-url-shortener-playground/blob/master/requirements.txt

$ python manage.py migrate
$ python manage.py runserver
```

## SQL DB setup
```sql
CREATE TABLE "url_shorten_urls" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, # Automatically set by Django
"date_created" datetime NOT NULL,
"original_url" varchar(65) NOT NULL,
"shortened_slug" varchar(65) NOT NULL,
```
## Features

* Extensive test coverage (unit & integration)
* URL shortener using Django libraries

## Contributing

I love contributions, so please feel free to fix bugs, improve things, provide documentation. Just send a pull request.
