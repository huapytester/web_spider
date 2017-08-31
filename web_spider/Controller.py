# -*- coding:utf-8 -*-

from scrapy import cmdline
import os
import sys


# 把项目的根目录加到环境变量
project_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_path)
# print(project_path)

# 通过scrapy的命令行工具执行scrapy的项目
cmdline.execute(['scrapy', 'crawl', 'jobbole'])

