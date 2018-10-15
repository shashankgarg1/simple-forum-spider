import scrapy
from scrapy.utils.markup import remove_tags
import re

multSpace = re.compile(r'\s\s+')
startSpace = re.compile(r'^\s+')
endSpace = re.compile(r'\s+$')
multDots = re.compile(r'\.\.\.\.\.+') #more than four periods
newlines = re.compile(r'\s*\n\s*')

def shrinkSpace(s):
    """turns multipel spaces into 1"""
    s = multSpace.sub(' ',s)
    s = multDots.sub('....',s)
    s = endSpace.sub('',s)
    s = startSpace.sub('',s)
    s = newlines.sub(' <NEWLINE> ',s)
    return s

class MessageBoardSpider(scrapy.Spider):
    name = "forum"
    allowed_domains= ["www.myproana.com"]
    start_urls = [
        'https://www.myproana.com/index.php/forum/58-bed-discussions/',
    ]

    self.thread_page = 'td.col_f_content'
    self.next_thread_page = 'li.next a::attr(href)'
    
    # comment parsing details
    self.comment = 'div.post_block'
    self.comment_text = 'div.post.entry-content'
    self.next_comment_page = 'li.next a::attr(href)'
    self.thread_link = 'span.post_id.right.ipsType_small.desc.blend_links a::attr(href)'
    self.post_id = 'div.post_block::attr(id)'
    self.date = 'abbr.published::text'
    self.user_name = 'p.member_title::text'


    def parse(self, response):
        # follow links to thread pages
        for href in response.css(self.thread_pages):
            yield response.follow(href.css('a::attr(href)').extract()[0], self.parse_thread)

        # follow pagination links
        next_page = response.css(self.next_thread_page).extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_thread(self, response):
        for quote in response.css(self.comment):
            paragraphs = quote.css(self.comment_text).extract()
            text = " ".join(remove_tags(paragraph) for paragraph in paragraphs)
            yield {
                'thread_link': quote.css(self.thread_link).extract(),
                'post_id': quote.css(self.post_id).extract(),
                'message': shrinkSpace(text),
                'date': quote.css(self.date).extract(),
                'user_name': quote.css(self.user_name).extract(),
            }

        next_page = response.css(self.next_comment_page).extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

