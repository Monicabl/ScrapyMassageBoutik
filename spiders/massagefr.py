from email.quoprimime import quote
from os import link
from unicodedata import name
from urllib import response
from numpy import product
import scrapy
class QuotesSpuder(scrapy.Spider):
    name = "massagefr"
    counter = 0    
    def countproducts(self, x):
        self.counter = self.counter + x
        print(self.counter)
        
    def start_requests(self):
        urls=[  

            'https://massageboutik.com/fr/183-magasiner-tout-produits-massage-boutik'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        next_page = response.css ('div.product-image-container a')
        link = response.css('div.product-image-container a::attr(href)').get()
        link = response.urljoin(link)
        yield from response.follow_all(next_page, self.parse_title)

        pagination_link = response.css('ul.pagination li a')
        yield from response.follow_all(pagination_link, self.parse)


    def parse_title(self, response):
        self.countproducts(1)
        
        for quote in response.css(".columns-container"):
            product = quote.css("h1::text").get()
            if quote.css("div.short-description p::text").get() is not None:
                description = quote.css("div.short-description *::text").getall()
            else:
                description = 'Acheter ' + product + ' de Massage Boutik'

            yield {
                'identifiant' : (f"Mafr{self.counter}"),
                'titre' : product,
                'description' : description,
                'lien': response.url,
                'état' : 'new',
                'prix': 'CAD'+quote.css("span.price::text").get() ,
                'disponibilité' : 'In Stock',
                'lien image' : quote.css(".pb-left-column div#image-block span#view_full_size img").xpath('@src').get(),
                'gtin':'',
                'référence fabricant' : quote.css("div.referencesmm #product_reference .editable::text").get(),
                'marque' : quote.css("div.referencesmm p#brand span a::text").get(), 
                #'color': quote.css('ul#color_to_pick_list li *::attr(name)').getall()
            }