# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from web_spider.items import BolePythonItem
from scrapy.loader import ItemLoader
from custom.url_md5 import url_md5
from web_spider.items import ArticelItemLoader

'''
1、设置所有python文章的首页为开始url
2、解析文章列表页的文章详情url和下一页的url
3、文章详情页的url交给scrapy下载，并回调字段解析函数
4、下一页的url交给scrapy下载，回调列表url解析函数
'''


class JobboleSpider(scrapy.Spider):

    # spider名称
    name = 'jobbole'
    # 爬取限制的域名
    allowed_domains = ['python.jobbole.com']
    # 开始爬取的url
    start_urls = ['http://python.jobbole.com/all-posts/']

    def parse(self, response):
        # 获取页面上所有的url
        post_nodes = response.css('#archive .post-thumb a')
        for post_node in post_nodes:
            # 二次select
            front_image_url = post_node.css('img::attr(src)').extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')
            # 使用parse模块拼接url的域名和地址
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': parse.urljoin(response.url, front_image_url)}, callback=self.parse_field)
        # 获取下一页的url
        # next_url = response.css('.margin-20 .next.page-numbers::attr(href)').extract_first()
        # print(next_url)
        # if next_url:
        #     # 处理下一页的列表页
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    # 使用css选择器提取字段
    def parse_field(self, response):

        # title = response.css('.entry-header h1::text').extract_first()
        # create_date = response.css('.entry-meta-hide-on-mobile::text').extract_first().replace('·', '').strip()
        # agree_num = response.css('.vote-post-up h10::text').extract_first()
        # comment_num = response.css('a[href="#article-comment"] span::text').extract_first()
        # fav_num = response.css('.bookmark-btn::text').extract_first()
        # content = response.css('div.entry').extract_first()
        # tags = ','.join(response.css('.entry-meta a::text').extract_first())
        # article_url = response.url
        # url_object_id = ''

        # # 实例化item对象
        # My_item = BolePythonItem()
        # # 填充item的字段
        # My_item['title'] = title
        # My_item['create_date'] = create_date
        # My_item['agree_num'] = agree_num
        # My_item['comment_num'] = comment_num
        # My_item['fav_num'] = fav_num
        # My_item['content'] = content
        # My_item['tags'] = tags
        #
        # # 返回一个填充好的item的实例
        # return My_item

        # 使用itemload保存数据
        item_load = ArticelItemLoader(item=BolePythonItem(), response=response)
        item_load.add_css('title', '.entry-header h1::text')
        item_load.add_css('create_date', '.entry-meta-hide-on-mobile::text')
        item_load.add_css('agree_num', '.vote-post-up h10::text')
        item_load.add_css('comment_num', 'a[href="#article-comment"] span::text')
        item_load.add_css('fav_num', '.bookmark-btn::text')
        item_load.add_css('content', 'div.entry')
        item_load.add_css('tags', '.entry-meta a::text')
        item_load.add_value('article_url', response.url)
        item_load.add_value('url_object_id', url_md5(response.url))
        item_load.add_value('front_image_url', response.meta.get('front_image_url', ''))

        article_item = item_load.load_item()
        yield article_item





