## Crawler for WirVsVirus Hackathon

This [scrapy](https://docs.scrapy.org/en/latest/index.html) crawler downloads all project submission detail pages
from DevPost gallery pages for the  [WirVsVirus Hackathon](https://wirvsvirushackathon.devpost.com/submissions).

It was motivated to get a complete overview about the projects
submitted to the Hackathon, and written by [Niko Schmuck](https://github.com/nikos)
please get in contact for any questions you have.

### How to use

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
$ python3 -m spacy download en_core_web_sm
$ make requirements
```

Then run (please be aware it can take several minutes to have all 1200+ pages crawled)

```
$ make run
```

Or specify HACKATHON the name of the hackathon as written in the url on devpost (e.g. 'wirvsvirushackathon' in [wirvsvirushackathon.devpost.com](wirvsvirushackathon.devpost.com))

```
$ make run HACKATHON=wirvsvirushackathon
```

See results of submissions as [JSON lines](http://jsonlines.org/) file generated with run in `item.jl`. 
