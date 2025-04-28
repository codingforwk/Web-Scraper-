import scrapy
from ..items import BbcHeadlineItem

class BbcNewsSpider(scrapy.Spider):
    name = "bbc_news"
    allowed_domains = ["bbc.com"]
    start_urls = ["https://www.bbc.com/news"]

    def parse(self, response):
        # Select the Top Stories section using updated selector
        top_section = response.css('div[aria-labelledby="Top-stories"]') or response.css('section[data-testid="top-stories"]')
        
        # Loop through each headline block
        for article in top_section.css('div.gs-c-promo'):
            item = BbcHeadlineItem()
            
            # Updated headline selector with fallback
            item["headline"] = article.css('h3.gs-c-promo-heading__title::text, h2.gs-c-promo-heading__title::text').get()
            
            # Updated URL selector
            relative_url = article.css('a.gs-c-promo-heading::attr(href)').get()
            if relative_url:
                item["url"] = response.urljoin(relative_url)
            
            # Updated summary selector
            item["summary"] = article.css('p.gs-c-promo-summary::text, p.ssrcss-1q0x1qg-Paragraph.e1jhz7w10::text').get(default="").strip()
            
            # Updated category selector
            item["category"] = article.css('a.gs-c-section-link::text, a.ssrcss-1k01hzj-StyledLink.ed0g1kj0::text').get(default="").strip()
            
            # Only yield if we have a headline
            if item["headline"]:
                yield item