import scrapy


class MyFirstSpider(scrapy.Spider):
    name = "swimming"
    start_urls = [
        'https://en.wikipedia.org/wiki/Swimming_(sport)',
        'https://en.wikipedia.org/wiki/Swimming',
        'https://dmoz-odp.org/Sports/Water_Sports/Swimming_and_Diving/',
        'https://www.britannica.com/sports/swimming-sport',
        'https://www.usaswimming.org/',
        'https://olympics.com/en/sports/swimming/',
        'https://swimswam.com/',
        'https://www.swimming.ca/en/',
        'https://www.specialolympics.org/what-we-do/sports/swimming',
        'https://www.swimmingworldmagazine.com/',
        'https://www.goswim.tv/',
        'https://www.swimming.org/',
    ]

    def parse(self, response):
        # first extract title of page
        title = response.css('title::text').get()
        yield {
            'title': title,
            'url': response.url
        }
        # now follow links to other pages
        for href in response.css('li a::attr(href)').getall():
            yield response.follow(href, callback=self.parse)
