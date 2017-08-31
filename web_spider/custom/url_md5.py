# -*- coding:utf-8 -*-
import hashlib
import re


def url_md5(url):
    # md5方法不支持unicode编码,需要转换成utf-8
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def get_num(arg):
    r = re.match('.*(\d+).*', arg)
    print(r.group(1))

get_num(' 6 收藏')
