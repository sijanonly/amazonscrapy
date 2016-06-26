### Why Scrapy Framework.

##### There are lots of tool out there like : BeautifulSoup, lxml for parsing html(web pages). But Scrapy gives you the whole framework. It allows you 
	###### 1. to define the spider (bot), 
	###### 2. to define the items (item to be scraped)
	###### 3. to define data storing module (pipelines) : where you can dump your data to simple csv file to connect data to your database operations

### Amazon Scraping

#### The spider will go through the UPC values and iterate over individual pages for extract the information.
#### The spider will scrape following attributes : length, breadth, height, shipping weight, production description, rank, asin number, image urls