# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SongItem(scrapy.Item):
    title = scrapy.Field()
    artist_url = scrapy.Field()
    artist_name = scrapy.Field()

    lyric_blocks = scrapy.Field()

    views = scrapy.Field()
    release_date = scrapy.Field()
    genre = scrapy.Field()

class ArtistItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    genre = scrapy.Field()
    views = scrapy.Field()
    
    songs_urls = scrapy.Field()
    related_artists_urls = scrapy.Field()
