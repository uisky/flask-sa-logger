import os
import logging
import pprint
import sqlparse
import re
from collections import OrderedDict
import colors
from flask import g, current_app


def term_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(columns), int(rows)


def format_sql(sql):
    sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
    sql = re.sub(r'(FROM|JOIN|UPDATE|INTO)\s+(\w+)', r'\1 ' + colors.magenta(r'\2', style='bold'), sql)

    keywords = (
        'SELECT', 'FROM', 'LEFT', 'RIGHT', 'INNER', 'UNION', 'ALL', 'JOIN', 'GROUP', 'BY',
        'HAVING', 'INSERT', 'UPDATE', 'CREATE TABLE', 'DELETE', 'VALUES', 'BEGIN', 'COMMIT', 'ROLLBACK',
        'LIMIT', 'OFFSET', 'WHERE', 'OUTER', 'CAST', 'ORDER', ' AS ', ' ON '
    )
    # '\033[1;32m{}\033[0;32m'.format(k)
    rep = {re.escape(k): colors.green(k, style='bold') for k in keywords}
    pattern = re.compile('|'.join(rep.keys()))

    return pattern.sub(lambda m: rep[re.escape(m.group(0))], sql)


def _init_stats():
    setattr(g, current_app.config.get('FLASK_SA_LOGGER_KEY'), OrderedDict())


class AlchemyLogFormatter(logging.Formatter):
    def format(self, record):
        if record.msg == '%r':
            # Это, скорее всего, параметры запроса пришли
            msg = colors.blue(pprint.pformat(record.args[0], indent=4))
        else:
            # А это сам запрос
            msg = record.getMessage()
            msg = '\n\n' + format_sql(msg)

        return msg


class AlchemyMemorizer(logging.Handler):
    def emit(self, record):
        if current_app.config.get('FLASK_SA_LOGGER_KEY') not in g:
            _init_stats()

        if record.msg != '%r':
            sql = format_sql(record.getMessage().strip())
            stats = g.get(current_app.config.get('FLASK_SA_LOGGER_KEY'))
            if sql in stats:
                stats[sql] += 1
            else:
                stats[sql] = 1

        return ''


def init_logging(app):
    level = app.config.get('FLASK_SA_LOGGER', False)

    if 'FLASK_SA_LOGGER_KEY' not in app.config:
        app.config['FLASK_SA_LOGGER_KEY'] = '_flask_sa_data'

    if not level:
        return

    db_logger = logging.getLogger('sqlalchemy.engine')
    db_logger.setLevel(logging.INFO)

    if level in (True, 'log'):
        db_handler = logging.StreamHandler()
        db_handler.setFormatter(AlchemyLogFormatter())
        db_logger.addHandler(db_handler)
    elif level in ('analyze', 'analyse'):
        db_handler = AlchemyMemorizer()
        db_logger.addHandler(db_handler)

        app.before_request(_init_stats)

        @app.after_request
        def track_sql_finish(response):
            stat = g.get(app.config.get('FLASK_SA_LOGGER_KEY'), [])
            w, _ = term_size()

            for sql, cnt in stat.items():
                print('-' * w)

                s_cnt = str(cnt)
                if cnt >= 5:
                    s_cnt = colors.red(s_cnt)
                elif cnt > 1:
                    s_cnt = colors.yellow(s_cnt)

                for i, line in enumerate(sql.split('\n')):
                    if i == 0:
                        print('%4s | %s' % (s_cnt, line))
                    else:
                        print('     | %s' % (line, ))

            print(colors.red('==== [ %4d total ]%s' % (sum(stat.values()), '=' * (w - 19))))

            return response
