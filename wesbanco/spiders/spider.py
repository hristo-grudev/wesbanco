import scrapy

from scrapy.loader import ItemLoader

from ..items import WesbancoItem
from itemloaders.processors import TakeFirst

base = 'https://www.wesbanco.com/education-insights/?fwp_paged={}'


class WesbancoSpider(scrapy.Spider):
	name = 'wesbanco'
	page = 1
	start_urls = [base.format(page)]

	def parse(self, response):
		post_links = response.xpath('//a[@class="v-post-card "]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		if post_links:
			self.page += 1
			yield response.follow(base.format(self.page), self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="v-content__text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=WesbancoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
