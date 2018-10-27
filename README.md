# simple-forum-spider

A simple Scrapy spider for scraping threads / comments from a single forum.

## Usage

Write output to csv:

```bash
cd simple-forum-spider
scrapy crawl forum -o my_forum.csv
```

## Modifications

To change the forum you must edit the `MessageBoardSpider` class in `forums/spiders/forum_spider.py`:

```python
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
```
You should also edit the `parse` method which is the default callback method for scrapy response objects.

Note that `www.sparkpeople.com` has multiple subforums but we are only looking at `https://www.sparkpeople.com/myspark/messageboard_topics.asp?imboard=7`.

## Dependencies
- [Scrapy](https://doc.scrapy.org/en/latest/)