import scrapy


class QuoteSpider(scrapy.Spider):
    name = "QuoteSpider"
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

from scrapy.crawler import CrawlerProcess
process = CrawlerProcess(settings={'FEEDS': {'Quotes.csv': {'format': 'csv'}}})
process.crawl(QuoteSpider)
process.start()