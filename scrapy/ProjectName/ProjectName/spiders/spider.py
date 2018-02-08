# -*- coding: utf-8 -*-
import scrapy
import time
import re

from random import randint
from ProjectName.items import ProjectnameItem

#-- Deprecated : from scrapy.contrib.spiders import CrawlSpider
from scrapy.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request

start_page = 1
end_page = 1811


class SpidernameSpider( CrawlSpider ):
	name = 'milemoa'
	allowed_domains = ['milemoa.com']
	start_urls = [ 'https://www.milemoa.com/bbs/index.php?mid=board&page=1' ]

	def parse(self, response):
		global start_page, end_page
		hxs = HtmlXPathSelector( response )
		print '** HXS:', hxs
		anchors = hxs.select( '//table[@id="lb_index"]' ).select( './tbody[@class="lb-document"]' ).select( './/td[@class="lb-in-td lb-title lb-in-no_webzine"]' )
		print
		seq = 0
		for A in anchors:
			seq += 1
			print "** SEQ:", seq
			item = ProjectnameItem()
			item['title'] = A.select( './h3[@class="lb-in-title"]/a[@class="lb-in-title lb-link"]/text()' ).extract()[0]
			item['title'] = item['title'].replace("\t", "").replace("\n", "")
			item['link'] = A.select( './h3[@class="lb-in-title"]/a[@class="lb-in-title lb-link"]/@href' ).extract()[0]
			item['desc'] = A.select( './h3[@class="lb-in-title"]/a[@class="lb-in-title lb-link"]/@title' ).extract()[0]
			yield item
		else:
			sleepsec = randint(1, 5);
			print '\t** <{}> Page ** Crawling Done. <{}> seconds got sleep -'.format( start_page, sleepsec )
			time.sleep( sleepsec )
			if( start_page <= end_page ):
			start_page += 1
			next_urls = [ 'https://www.milemoa.com/bbs/index.php?mid=board&page=' + str(start_page) ]
			yield Request( next_urls[0], self.parse )
		pass
	pass
