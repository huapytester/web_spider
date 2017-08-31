# -*- coding: utf-8 -*-

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
import MySQLdb
import csv
import sys
import os


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WebSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 自定义pipeline
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for status, value in results:
            image_path = value['path']
            print(results)
            item['image_path'] = image_path
        return item


class JsonPipeline(object):
    # 自定义数据保存到json文件
    def __init__(self):
        self.json_file = codecs.open('article.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False, indent=4) + '\n'
        self.json_file.write(lines)
        return item

    def close_spider(self, spider):
        self.json_file.close()


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.Connect('localhost', 'root', '1111', 'web_spider', 3306)
        self.cursor = self.conn.cursor()
        self.conn.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_python(title, create_date)
            VALUES (%s, %s)
        """ % (item['title'], item['create_date'],)
        self.cursor.execute(insert_sql)
        self.conn.commit()
        pass
    '''insert_sql = """
            insert into jobbole_python(title, create_date, agree_num,comment_num,fav_num,content,tags,article_url,url_object_id,front_image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql %
                            (item['title'], item['create_date'], item['agree_num'], item['comment_num'],
                             item['fav_num'], item['content'],item['tags'], item['article_url'],
                             item['url_object_id'], item['front_image_url'][0]))'''







