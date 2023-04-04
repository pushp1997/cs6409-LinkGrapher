import os
import scrapy
from typing import Set, List
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class LinkFinderSpider(scrapy.Spider):
    name = "linkFinderSpider"
    start_urls: List[str] = ["http://www.cs.ucc.ie/~hoare/page1.html"]
    visited_urls: Set[str] = set()

    # Define the rules for following links
    rules = (Rule(LinkExtractor(), callback="parse", follow=True),)

    def parse(self, response):
        # Get the source URL
        url = response.url

        # Since href only has page2.html and not the complete address
        base_address = "/".join(url.split("/")[:-1])

        if url in self.visited_urls:
            self.logger.info(f"Skipping already visited URL: {url}")
            yield None
        else:
            self.visited_urls.add(url)
            item = {}
            item["url"] = url
            # Get the destination URLs / URLs in the webpage's body
            links = response.css("a::attr(href)").getall()
            item["links"] = ["/".join([base_address, link]) for link in links]
            yield item
            yield from response.follow_all(links, callback=self.parse)
