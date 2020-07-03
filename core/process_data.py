import re
from urllib.parse import quote

from config import TITLE_MIN_LENGTH
from config import CONTENT_MIN_LENGTH
from config import DESCRIBE_REPLACE_STRING
from config import ARTICLE_DESCRIPTION_LENGTH


def quote_data(title: str, content: str, new_img_lists: list) -> tuple:
    """编码数据并提取出描述信息"""

    # 提取描述信息
    description = re.sub(r'<.+?>', '', content, flags=re.S)
    for string in DESCRIBE_REPLACE_STRING:
        description = description.replace(string, '')

    # 替换图片链接
    for old_link, now_link in new_img_lists:
        content = content.replace(old_link, now_link)

    title = quote(title)
    content = quote(content)
    description = quote(description[:ARTICLE_DESCRIPTION_LENGTH])

    return title, content, description


def check_data(title: str, content: str) -> bool:
    """校验数据（未使用）"""

    # 过滤字符串
    content = re.sub(r'<.+?>', '', content, flags=re.S)
    for string in DESCRIBE_REPLACE_STRING:
        content = content.replace(string, '')

    if len(title) < TITLE_MIN_LENGTH:
        return False
    if len(content)< CONTENT_MIN_LENGTH:
        return False

    return True
