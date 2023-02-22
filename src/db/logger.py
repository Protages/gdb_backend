import time
import logging

from sqlalchemy import event

from src.db.database import engine


logging.basicConfig()
logger = logging.getLogger('query')
logger.setLevel(logging.DEBUG)


@event.listens_for(engine, 'before_cursor_execute')
def before_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    conn.info.setdefault('query_start_time', []).append(time.time())
    p = ', '.join(str(p) for p in parameters)
    msg = p + '\n' + '=' * 80 + f'\n{statement}\n'
    logger.debug(' ' + msg)


@event.listens_for(engine, 'after_cursor_execute')
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    msg = f'Total Time: {total}\n' + '=' * 80 + '\n'
    logger.debug(' ' + msg)
