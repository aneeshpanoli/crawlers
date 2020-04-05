## Crawler for WirVsVirus Hackathon

This [scrapy](https://docs.scrapy.org/en/latest/index.html) crawler downloads all project submission detail pages
from DevPost gallery pages for the  [WirVsVirus Hackathon](https://wirvsvirushackathon.devpost.com/submissions).

It was motivated to get an complete overview about the projects
submitted to the Hackathon, and written by [Niko Schmuck](https://github.com/nikos)
please get in contact for any questsions you have.

### How to use

Please ensure that you have a working Python 3.x setup installed.
Create an virtualenv (I prefer [virtualenv-wrapper](https://virtualenvwrapper.readthedocs.org/en/latest/ "virtualenv-wrapper")):

```
$ mkvirtualenv DevPostCrawler
```

And install requirements:

```
$ make requirements
```

Then run (please be aware that it will take some minutes to have all 1200+ pages crawled)

```
$ make run
```

See results of submissions as [JSON lines](http://jsonlines.org/) file generated with run in `item.jl`. 