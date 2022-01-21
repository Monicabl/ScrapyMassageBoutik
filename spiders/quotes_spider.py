from unicodedata import name
from urllib import response
import scrapy
class QuotesSpuder(scrapy.Spider):
    name = "quotes"
    counter = 0    
    def countproducts(self, x):
        self.counter = self.counter + x
        print(self.counter)
        
    def start_requests(self):
        urls=[
            # 'https://massageboutik.com/en/massage-table/10-expresso-nomad-table.html'
            'https://massageboutik.com/en/183-shop-by-category-massage-boutik-products'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        next_page = response.css ('div.product-image-container a')
        yield from response.follow_all(next_page, self.parse_title)

        # pagination_link = response.css('ul.pagination li a')
        # yield from response.follow_all(pagination_link, self.parse)


    def parse_title(self, response):
        self.countproducts(1)
        for quote in response.css(".pb-center-column"):

            yield {
                'id' : (f"Mass{self.counter}"),
                'title' : quote.css("h1::text").get(),
                'description' : ,
                'link':,
                'condition' : 'new',
                'price': ,
                'availability' : 'In Stock',
                'image link' : ,
                'gtin':,
                'mpn' : '',
                'brand' : ,

            }