import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
import urllib2
import json
# from urllib.parse import urlparse
# from scrapy.utils.response import get_base_url
# scrapy crawl amazon -t csv -o Amazon.csv --loglevel=INFO

from AmazonScrapy.items import AmazonscrapyItem


class AmazonSpider(CrawlSpider):
    name = "AmazonSpider"
    allowed_domains = ["www.amazon.com"]
    start_urls = [
        'http://www.amazon.com',
    ]

    def parse_start_url(self, response):
        all_links = []
        # upc_list = ['045663158200']
        with open('./AmazonScrapy/upclist.txt') as f:
            content = f.read().split(',')
        upc_list = list(map(lambda x:x.strip(),content))
        print "upc_list", upc_list
        for each_upc in upc_list:
            full_url = "http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+each_upc
            print("full url", full_url)
            all_links.append(scrapy.Request(
                full_url,
                self.parse_lists))
        return all_links

    def parse_lists(self, response):
        print "response", response.url
        all_item_links = []
        sel = Selector(response)
        item_links = sel.xpath("//div[@id='resultsCol']//ul//li[contains(@id,'result')]//a[contains(@class,'s-access-detail-page')]/@href")
        # with open('test.html','wb') as f:
        #     f.write(response.body)
        for each_link in item_links:
            print "each_link", each_link.extract()
            my_request = scrapy.Request(
                each_link.extract(),
                self.parse_items)
            all_item_links.append(my_request)

        return all_item_links

    def parse_items(self, response):
        print "........................"
        print "entered items", response.url
        print "........................"
        sel = Selector(response)
        image_urls = sel.xpath("//div[@class='imgTagWrapper']//img/@src").extract_first()
        description = sel.xpath("//div[@class='productDescriptionWrapper']/text()").extract_first().strip()
        # with open('test1.html','wb') as f:
        #     f.write(response.body)
        image_urls = [str(image_urls)]
        # print "description", description
        product_details = sel.xpath('//div[@id="detail-bullets"]//table//div[@class="content"]//ul//li[not(@id = "SalesRank") and not(@class="zg_hrsr_item") ][position()<8]')
        # print "product_dimension", product_details[0].extract()
        product_details_dict = {
            'product_dimensions': None,
            'shipping_weight': None,
            'product_description': None,
            'domestic_shipping': None,
            'international_shipping': None,
            'shipping_advisory': None,
            'asin': None,
            'item_model_number': None,
            'image_urls': None

        }
        product_details_dict['product_description'] = description
        product_details_dict['image_urls'] = image_urls
        for each in product_details:
            item_property = each.xpath("./b/text()").extract_first().strip().replace('\n','').replace('\t','').replace(':', '').lower()
            item_property = item_property.split(' ')
            item_property = "_".join(item_property)
            item_value = each.xpath("./text()").extract_first().strip().replace('\n','').replace('\t','').replace(':', '').replace('(', '')
            product_details_dict[item_property] = item_value
            # print "item_property", item_property, item_value

        # if product_details_dict['product_dimensions'] is None:
        #     pro_description = description.lower()
        #     words = pro_description.split() #split the sentence into individual words
        #     # try:
        #     dimension_upper = sel.xpath('//div[@id="feature-bullets"]//ul//li[contains(normalize-space(string(self::li)),"Dimension")]/text()').extract_first()
        #     print "dimension_upper", dimension_upper
        #     # except:
        #     #     pass

        item = AmazonscrapyItem(
            product_dimensions=product_details_dict['product_dimensions'],
            shipping_weight=product_details_dict['shipping_weight'],
            product_description=product_details_dict['product_description'],
            domestic_shipping=product_details_dict['domestic_shipping'],
            international_shipping=product_details_dict['international_shipping'],
            shipping_advisory=product_details_dict['shipping_advisory'],
            asin=product_details_dict['asin'],
            item_model_number=product_details_dict['item_model_number'],
            image_urls=product_details_dict['image_urls']
        )
        yield item



