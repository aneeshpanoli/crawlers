## Crawler for DevPost Hackathons

This [scrapy](https://docs.scrapy.org/en/latest/index.html) crawler downloads all project submission detail pages
from DevPost gallery pages, for example: [WirVsVirus Hackathon](https://wirvsvirushackathon.devpost.com/submissions).

It was motivated to get a complete overview about the projects
submitted to the Hackathon, and written by [Niko Schmuck](https://github.com/nikos)
please get in contact for any questions you have.

### Setup

Please ensure that you have a working Python 3.x setup installed.
Create a virtualenv (you might want to check [virtualenv-wrapper](https://virtualenvwrapper.readthedocs.org/en/latest/ "virtualenv-wrapper")):

```
$ python3 -m venv venv
```

Activate the virtualenv:
```
$ source venv/bin/activate
```

And install requirements:

```
$ make requirements
```

#### Language Translations

If you want to crawl hackathons which are not described in english, your story text will be translated
to english with Google Cloud translation API. It is required that you set `GOOGLE_APPLICATION_CREDENTIALS`
to the JSON key file properly.

#### Elasticsearch support

The crawler will try not only to save the items to JSON lines file, but also to add the documents to
an full-text index for further analysis. To start up a docker container with Elasticsearch 
copy the `.env-sample` to `.env` and adapt to your local needs, then you spin up the containers with:

```
$ docker-compose up -d
```


### Use the crawler

If you have set up your system as described above, you should be able to 
run (please be aware it can take several minutes to have all 1200+ pages crawled)

```
$ make run
```

Or specify HACKATHON the name of the hackathon as written in the url on devpost (e.g. 'wirvsvirushackathon' in [wirvsvirushackathon.devpost.com](wirvsvirushackathon.devpost.com))

```
$ make run HACKATHON=wirvsvirushackathon
```

See results of submissions as [JSON lines](http://jsonlines.org/) file generated with run in `item.jl`. 
