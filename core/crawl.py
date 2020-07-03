import os
import re
import ssl
import uuid
import time
import requests
from lxml import etree
from urllib.error import HTTPError
from urllib.request import urlretrieve

from tools import gen_path
from .db_oper import fetch_title

from config import HELLO_WORLD_DB

# 全局取消证书验证（使用python urllib时出现[SSL: CERTIFICATE_VERIFY_FAILED]报错的解决方案）
ssl._create_default_https_context = ssl._create_unverified_context

_headers = {
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Cookie': '_ga=GA1.2.652266828.1566468177; __gads=ID=dd446a503ec0d197:T=1566468176:S=ALNI_MYgfSezudu4OToyD7xN_N63qzY_pw; _gid=GA1.2.386478030.1566782044; .Cnblogs.AspNetCore.Cookies=CfDJ8BQYbW6Qx5RFuF4UTI7QvU0orntNuBsEs3kTesU79Itw44F1jk4d7DTmwjKR5_zjhW-STlyeKRFwhwlKZa_idcHzqfvDT4c4-zeDPSK4uIba74c6smrHCzqKO3Fu4Q2P11HET8YUn4W134XXizJwff9WerFTkmLM6_TpdahMS8QGiH53koqfRH84TXaN_a7T8PlNWljHFSMXS7aXAEB3Mv80VxKKgnQoIvm9CFEua-BBpMqVVxppVOYvUno3JBiEOOI-iyrF4kw7kXuf7EB_XUZ26Bg9Ps861rvTg8lHC6xWO3gBy7YT26KPhPBKeqZLEPMJEfdEYktBXlkU184WZQFapgmPFkOp5hEL1y9l8H-WmE-NzLoHLRVg3cMCRtMO6_URVKxQBfmRDYhMZkAuvZirZAlN2Xpn69dc1ApE22EkeKB4EjH--g-MNkC8ONHsWw; .CNBlogsCookie=28454F1F5B3B9D9FF9649D0AC0355B9912690ADEB2082DDB0416346AF84B59A02532393462CB8D38F91918FF40174E2A7527B962F4072FEAFDD557CC167E7C48E64FF0EE155CF075B0BC22779C04D1229C5706D8',
}


def crawl_first(link: str) -> list:
    """提取文档链接"""
    links = []
    res = requests.get(link, headers=_headers)
    tree = etree.HTML(res.text)

    # 提取文章链接
    for blog in tree.xpath('.//div[@class="post_item"]'):
        title = blog.xpath('.//div[@class="post_item_body"]/h3/a/text()')[0]
        if fetch_title(title):
            continue
        link = blog.xpath('.//div[@class="post_item_body"]/h3/a/@href')[0]
        links.append((title, link))

    return links


def crawl_second(link: str):
    """提取文档内容"""
    res = requests.get(link, headers=_headers)

    # 解析提取文章内容及图片链接
    content = re.search(
        f'(<div id="cnblogs_post_body".+?)<div id="MySignature"',
        res.text, re.S).group(1)
    img_links = re.findall(
        r'"(https://img\d{4}.cnblogs.com/blog/.+?)"', content, re.S)

    return content, img_links


def down_img(img_link: str, img_link_map: list):
    """下载图片并返回新的图片链接"""
    try:
        img_name = f'{str(uuid.uuid4())}.png'
        year_month = time.strftime('%Y-%m')
        now_ai_dir = gen_path(HELLO_WORLD_DB, 'media/ai', year_month)
        img_path = gen_path(now_ai_dir, img_name)

        # 若目录不存在，则创建目录
        os.path.exists(now_ai_dir) or os.mkdir(now_ai_dir)

        try:
            # 开始下载图片
            urlretrieve(img_link, img_path)

            # 将完工的图片链接添加到就绪队列
            img_link_map.append((img_link, f'/media/ai/{year_month}/{img_name}'))

        except HTTPError as e:
            # 下载出错则删除未成功下载的图片
            os.remove(img_path)
            print(e)

    except Exception as e:
        print(e)
