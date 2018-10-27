import scrapy
from scrapy.utils.markup import remove_tags
import re
import pdb

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

    def __init__(self):
        super(MessageBoardSpider, self)

        self.start_urls = [
            "https://www.sparkpeople.com/myspark/messageboard_topics.asp?imboard=7"
        ]

        self.allowed_domains= ["sparkpeople.com"]

        # self.thread_pages = 'div.topics_table_row'
        self.next_thread_page = 'a.next_page'
 
        # comment parsing details
        self.comment = 'div.main_table_row'
        # self.next_comment_page = 'a.next_page ::attr(href)'

    def parse(self, response):
        # follow links to thread pages
        thread_pages1 = response.xpath("//div[@id=\"forum\"]//div[@id=\"topics_table\"]/div[@class=\"topics_table_row\"]/div[@class=\"topics_table_cell row2 c1\"]/a/@href").extract()

        thread_pages2 = response.xpath("//div[@id=\"forum\"]//div[@id=\"topics_table\"]/div[@class=\"topics_table_row\"]/div[@class=\"topics_table_cell row1 c1\"]/a/@href").extract()

        thread_pages = thread_pages1 + thread_pages2

        for thread_page in thread_pages:
            if thread_page is not None:
                next_thread = response.urljoin(thread_page)
                yield response.follow(next_thread, callback=self.parse_thread)
       
        # follow pagination links
        try:
            next_pages = response.css(self.next_thread_page)
        except:
            return

        flag = False
        for next_page in next_pages:
            if "Next" in next_page.xpath("./text()").extract_first():
                flag = True
                break
        if not flag:
            return

        next_page = next_page.xpath("./@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_thread(self, response):
        thread_link = response.xpath("//head/meta[@property=\"og:url\"]/@content").extract_first()
        for quote in response.css(self.comment):
            # extract comment text in paragraphs
            paragraphs = quote.css('div.main_table_cell.ce2').css('div.mb_message').css('div.mb_message_text').extract()
            text = " ".join(remove_tags(paragraph) for paragraph in paragraphs)
            date = quote.css('div.main_table_cell.ce1').css('div.mb_author').css('div.mb_author_text').css('span.date_posted::text').extract_first()
            user_name = quote.css('div.main_table_cell.ce1').css('div.mb_author').css('div.mb_author_text').css('span.mb_user::text').extract_first()
            if user_name is not None and date is not None and text is not None:
                yield {
                    'thread_link': thread_link,
                    'message': shrinkSpace(text),
                    'date': date,
                    'user_name': user_name,
                    'post_id': user_name + date
                }



        # follow pagination links
        try:
            next_pages = response.css(self.next_thread_page)
        except:
            return

        flag = False
        for next_page in next_pages:
            if "Next" in next_page.xpath("./text()").extract_first():
                flag = True
                break
        if not flag:
            return


        next_page = next_page.xpath("./@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_thread)

