from email.quoprimime import quote
from os import link
from unicodedata import name
from urllib import response
from numpy import product
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
        link = response.css('div.product-image-container a::attr(href)').get()
        link = response.urljoin(link)
        yield from response.follow_all(next_page, self.parse_title)

        # pagination_link = response.css('ul.pagination li a')
        # yield from response.follow_all(pagination_link, self.parse)


    def parse_title(self, response):
        self.countproducts(1)
        for quote in response.css(".primary_block"):
            product = quote.css("h1::text").get()

            yield {
                'id' : (f"Mass{self.counter}"),
                'title' : product,
                'description' : 'Buy ' + product + ' from Massage Boutik',
                'link': response.url,
                'condition' : 'new',
                'price': quote.css("span.price::text").get() ,
                'availability' : 'In Stock',
                'image link' : quote.css(".pb-left-column div#image-block span#view_full_size img").xpath('@src').get(),
                'gtin':'',
                'mpn' : quote.css("div.referencesmm #product_reference .editable::text").get(),
                'brand' : quote.css("div.referencesmm p#brand span a::text").get()

            }