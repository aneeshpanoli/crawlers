# -*- coding: utf-8 -*-
import logging
import datetime
import re

import scrapy

from DevPostCrawler.items import DevPostCrawlerItem
from DevPostCrawler.utils.normalizer import normalize_title, normalize_challenge


class ProjectsSpider(scrapy.Spider):
    name = 'projects'

    allowed_domains = ['devpost.com']

    # Grep Youtube Video ID from embedded video player reference,
    # used inside gallery of submission detail page
    youtube_embed_regex = r"embed\/(.*)\?"
    vimeo_embed_regex = r"player.vimeo.com\/video\/(.*)\?"

    def __init__(self, hackathon=None, *args, **kwargs):
        super(ProjectsSpider, self).__init__(*args, **kwargs)
        self.start_url = 'https://%s.devpost.com/submissions' % hackathon

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse_start_page)

    def parse_start_page(self, response):
        # Search filter used on the right side bar to select category,
        # unfortunately category is not listed on submission detail page

        # Get all filters names in original order
        submission_filters = response.css('form.filter-submissions ul li:first-child input[name*="filter["]::attr(name)').getall()

        if submission_filters:
            # TODO also use other filters?  for submission_filter in submission_filters:
            challenge_filter = submission_filters[0]
            challenges = response.css(f'input[name="{challenge_filter}"]::attr(value)').getall()

            for challenge in challenges[:3]:  # TODO: ie. limit with [:9]
                yield scrapy.FormRequest.from_response(response,
                                                       formcss='form.filter-submissions',
                                                       formdata={challenge_filter: challenge},
                                                       callback=self.parse_gallery,
                                                       cb_kwargs={'challenge': challenge})
        # If no filter available
        else:
            yield scrapy.Request(url=self.start_url,
                                 callback=self.parse_gallery,
                                 cb_kwargs={'challenge': ''},
                                 dont_filter=True)

    def parse_gallery(self, response, challenge):
        item_urls = response.css('div.gallery-item a.link-to-software::attr(href)').getall()
        for item_url in item_urls:
            yield scrapy.Request(url=item_url,
                                 callback=self.parse_software_page,
                                 cb_kwargs={'challenge': challenge})
        # Look for more items on next page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            self.log(f"*** Visit next page for: {challenge}: {next_page}", level=logging.DEBUG)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,
                                 callback=self.parse_gallery,
                                 cb_kwargs={'challenge': challenge})

    def parse_software_page(self, response, challenge):
        item = DevPostCrawlerItem()

        item['title'] = normalize_title(response.css('h1#app-title::text').get()),
        item['subtitleOriginal'] = response.css('header p.large::text').get().strip(),
        item['hackathons'] = [s.strip() for s in response.css('.software-list-content a::text').getall()],
        item['url'] = response.url,
        item['category'] = normalize_challenge(challenge),
        item['image'] = response.css('meta[itemprop="image"]::attr(content)').get(),
        item['video'] = self.normalize_video_link(response.css('iframe.video-embed::attr(src)').get()),

        raw_txt = ''.join(response.css('#app-details-left div:not([id]):not([class]) ::text').getall()).strip()
        item['storyTextOriginal'] = self.strip_all_whitespaces(raw_txt),

        # item['storyHTML'] = response.css('#app-details-left div:not([id]):not([class])').get().strip(),
        app_links = response.css('nav.app-links a::attr(href)').getall()
        story_links = response.css('#app-details-left div:not([id]):not([class]) a::attr(href)').getall()
        item['links'] = list(set(app_links + story_links))

        item['nrLikes'] = self.normalize_int(response, 'a.like-button .side-count::text'),
        item['nrComments'] = self.normalize_int(response, 'a.comment-button .side-count::text'),
        item['nrHighlights'] = len(response.css('.winner').getall()),
        item['nrUpdates'] = self.normalize_int(response, 'a[href*="#updates"]:not([id]) .side-count::text'),
        item['lastUpdatedAt'] = response.css('time::attr(datetime)').get(),
        item['teamMembers'] = response.css('#app-team .user-profile-link ::text').getall(),
        item['builtWith'] = [s.strip().lower() for s in response.css('#built-with span.cp-tag ::text').getall()],
        item['scrapedAt'] = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),

        yield item

    def normalize_video_link(self, embed_link):
        if embed_link is None:
            return ''
        if 'youtube.' in embed_link:
            # https://www.youtube.com/embed/sLx3Yi5vll4?enablejsapi=1&hl=en_US&rel=0&start=3&version=3&wmode=transparent
            links = re.findall(self.youtube_embed_regex, embed_link)
            return '' if len(links) == 0 else f'https://www.youtube.com/watch?v={links[0]}'
        elif 'vimeo.' in embed_link:
            # https://player.vimeo.com/video/404234005?byline=0&portrait=0&title=0#t=
            links = re.findall(self.vimeo_embed_regex, embed_link)
            return '' if len(links) == 0 else f'https://vimeo.com/{links[0]}'
        else:
            return embed_link

    @staticmethod
    def strip_all_whitespaces(txt):
        return ' '.join(txt.split())

    @staticmethod
    def normalize_int(response, selector):
        value = response.css(selector).get()
        return 0 if value is None else value

    def parse(self, response):
        # Not required (see parse_software_page)
        pass
