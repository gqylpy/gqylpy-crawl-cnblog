from .config import IN_SERVER

if IN_SERVER:
    class DBS:
        # Database alias
        gqylpy = 'gqylpy'
        hello_world = 'hello_world'

        class Config:
            # Database Config
            gqylpy = dict(
                host='localhost',
                port=3380,
                user='gqy',
                password='user@gqy',
                db='gqylpy',
                charset='utf8',
                connect_timeout=60 * 60 * 24 * 15  # 15 Day
            )
            hello_world = dict(
                host='localhost',
                port=3380,
                user='hlwd',
                password='user@hlwd',
                db='hello_world',
                charset='utf8',
                connect_timeout=60 * 60 * 24 * 15
            )
else:
    class DBS:
        # Database alias
        gqylpy = 'gqylpy'
        hello_world = 'hello_world'

        class Config:
            # Database Config
            gqylpy = dict(
                host='',
                port='',
                user='',
                password='',
                db='gqylpy',
                charset='utf8',
                connect_timeout=60 * 60 * 24 * 15  # 15 Day
            )
            hello_world = dict(
                host='',
                port='',
                user='',
                password='',
                db='hello_world',
                charset='utf8',
                connect_timeout=60 * 60 * 24 * 15
            )
