# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import datetime
from scrapy.loader import ItemLoader
from scrapy.loader import processors


# 去掉提取数据中的空格
def take_out_blank(arg):
    return arg.strip()


# 更改日期格式
def date_convert(arg):
    try:
        create_date = datetime.datetime.strptime(arg, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


# 获取字符中的数字
def get_num(arg):
    r = re.match('.*(\d+).*', arg)
    if r:
        return int(r.group(1))
    else:
        return 0


# 去除多余的评论
def take_out_comment(arg):
    if arg.endswith(u' 评论 '):
        pass
    else:
        return arg


# 自定义itemloader
class ArticelItemLoader(ItemLoader):
    default_output_processor = processors.TakeFirst()

    pass


class BolePythonItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=processors.MapCompose(lambda x: x.replace(' ·', '').strip()),
    )
    agree_num = scrapy.Field(
        input_processor=processors.MapCompose(get_num),
    )
    comment_num = scrapy.Field(
        input_processor=processors.MapCompose(get_num),
    )
    fav_num = scrapy.Field(
        input_processor=processors.MapCompose(get_num),
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        # 输入到itemloader装置前，执行的函数
        input_processor=processors.MapCompose(take_out_comment),
        # itemloader数据存储到item执行的函数
        output_processor=processors.Join(',')
    )
    article_url = scrapy.Field(
        # output_processor=processors.Identity()
    )
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=processors.Identity()
    )
    image_path = scrapy.Field()
