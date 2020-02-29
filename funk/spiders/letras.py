import scrapy
from ..top_artists import top_artists 
from ..items import SongItem, ArtistItem

class LetrasSpider(scrapy.Spider):
    name = "letras"
    start_urls = top_artists
    
    FUNK_GENRE = "/estilos/funk/"

    def parse(self, response):
        artist_name = response.css('#cnt_top h1::text').get()
        genre = LetrasSpider.get_genre(response)
        print(artist_name)
        if genre != LetrasSpider.FUNK_GENRE:
            print('artist not a funk artist, don\'t scrape')
            return
        songs_urls = response.css('a.song-name::attr(href)').getall()
        for raw_url in songs_urls:
            song_url = response.urljoin(raw_url)
            yield scrapy.Request(url=song_url, callback=self.parse_lyrics_page)
        related_artists_urls = [response.urljoin(url) for url in response.css('.cnt-list-thumb a::attr(href)').getall()]
        for artist_url in related_artists_urls:
            yield scrapy.Request(url=artist_url, callback=self.parse)
        # item = ArtistItem(name=artist_name, genre=genre, songs_urls=songs_urls, related_artists_urls=related_artists_urls)
        # return item


    def parse_lyrics_page(self, response):
        title = response.css('.cnt-head_title h1::text').get()
        artist_url = response.css('.cnt-head_title > h2 > a::attr(href)').get()
        artist_name = response.css('.cnt-head_title > h2 > a::text').get()
        
        # old way, losing information of lyric blocks
        # lyric = response.css('.cnt-letra-trad p::text').getall()

        # new way, gets information of lyric blocks
        lyric_blocks = list(map(lambda x:x.replace('<p>','').replace('</p>','').split('<br>'), response.css('.cnt-letra-trad p').getall()))

        views = response.css('.cnt-info_exib b::text').get()
        release_date = response.css('span.metadata_unit-info--text_only::text').get()
        genre = LetrasSpider.get_genre(response)
        item = SongItem(
            title=title,
            artist_url=artist_url,
            artist_name=artist_name,
            lyric_blocks=list(lyric_blocks),
            views=views,
            release_date=release_date,
            genre=genre
        )
        return item
    
    @staticmethod
    def get_genre(response):
        return response.css('#breadcrumb > span:nth-child(2) > a::attr(href)').get()