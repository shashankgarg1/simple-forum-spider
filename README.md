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
```

Note that `www.myproana.com` has multiple subforums but we are only looking at `www.myproana.com/index.php/forum/58-bed-discussions`.

## Dependencies
- [Scrapy](https://doc.scrapy.org/en/latest/)