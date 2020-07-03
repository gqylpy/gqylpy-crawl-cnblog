import time
from concurrent.futures import ThreadPoolExecutor

from .crawl import down_img
from .crawl import crawl_first
from .crawl import crawl_second
from .db_oper import create_blog
from .process_data import quote_data

from config import WHILE_CYCLE
from config import DATETIME_FORMAT
from config import DOWN_IMG_POOL_NUMBER

_first_index = [
    'https://www.cnblogs.com/',  # 首页
    'https://www.cnblogs.com/candidate/'  # 候选
]


def main():
    ar_title: str
    ar_link: str

    while True:
        try:

            for link in _first_index:
                data: list = crawl_first(link)

                print(f'获取 {len(data)} 篇文章')

                for ar_title, ar_link in data:
                    try:
                        content, img_links = crawl_second(ar_link)
                    except Exception:
                        print(ar_title, '--❌')
                        continue

                    # 重置图片链接映射数据
                    img_link_map = []

                    # 下载图片
                    if img_links:
                        tp = ThreadPoolExecutor(DOWN_IMG_POOL_NUMBER)
                        [tp.submit(down_img, img_link, img_link_map) for img_link in img_links]
                        tp.shutdown()

                    # 编码数据并写入数据库
                    create_blog(*quote_data(ar_title, content, img_link_map))

                    print(ar_title, '--👌')

            print(f'Ctime: {time.strftime(DATETIME_FORMAT)}, wait ten: {WHILE_CYCLE}s')
            time.sleep(WHILE_CYCLE)

        except Exception as e:
            print(ar_title, ar_link, '--❌')
