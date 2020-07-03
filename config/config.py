import os


def _gen_path(*args: str) -> 'An absolute path':
    # Generate an absolute path.
    return os.path.abspath(os.path.join(*args))


BASE_DIR = _gen_path(os.path.dirname(os.path.dirname(__file__)))

DB_DIR = _gen_path(BASE_DIR, 'db')
LOG_DIR = _gen_path(BASE_DIR, 'log')

IN_SERVER = True

# 文件编码
FE = 'UTF-8'

DATETIME_FORMAT = '%F %T'

WHILE_CYCLE = 60 * 10

DOWN_IMG_POOL_NUMBER = 5

HELLO_WORLD_DB = '/data/hello_world/'

# 文档描述长度
ARTICLE_DESCRIPTION_LENGTH = 150

# 描述信息替换的字符
DESCRIBE_REPLACE_STRING = [' ', '\n', '\t', '&nbsp;', '# ']

# 赞范围
PRAISE_RANGE = 3, 15

# 访问量范围
VISIT_RANGE = 60, 300

# 文章标题、内容长度
TITLE_MIN_LENGTH = 4
CONTENT_MIN_LENGTH = 200

# 评论总数范围
COMMENT_COUNT_RANGE = 0, 6

# 评论日期追加0.2天至15天
COMMENT_TIME_ADD_DAY = 0.2, 15
