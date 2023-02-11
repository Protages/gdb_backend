import importlib
import os
import uuid
from collections import defaultdict, namedtuple
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional, Union

from alembic.config import Config
from sqlalchemy_utils import create_database, drop_database


PROJECT_PATH = Path(__file__).parent.parent.resolve()
# DEFAULT_PG_URL = 'postgresql://user:hackme@localhost/staff'
DEFAULT_SQLITE_URL = 'sqlite:///./sql_test.db'


def make_alembic_config(cmd_opts, base_path: str = PROJECT_PATH) -> Config:
    # Replace path to alembic.ini file to absolute
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(
        file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts
    )

    # Replace path to alembic folder to absolute
    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            'script_location', os.path.join(base_path, alembic_location)
        )
    if cmd_opts.pg_url:
        config.set_main_option('sqlalchemy.url', cmd_opts.pg_url)

    return config


def alembic_config_from_url(pg_url: str | None = None) -> Config:
    """
    Provides Python object, representing alembic.ini file.
    """
    cmd_options = SimpleNamespace(
        config='alembic.ini', name='alembic', pg_url=pg_url,
        raiseerr=False, x=None,
    )

    return make_alembic_config(cmd_options)


@contextmanager
def tmp_database(db_url, suffix: str = '', **kwargs):
    # For PostgreSQL
    # tmp_db_name = '.'.join([uuid.uuid4().hex, 'test', suffix])
    # tmp_db_url = str(db_url.with_path(tmp_db_name))
    
    tmp_db_url = db_url
    create_database(tmp_db_url, **kwargs)

    try:
        yield tmp_db_url
    finally:
        drop_database(tmp_db_url)


def check_dir_contain_files_with_extensions(path: str, extentions: tuple = ('.py',)):
    '''
    If directory or its subdirectories contain
    a file with specific extensions (.py), an error will be caused
    '''
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)

        if os.path.isdir(file_path):
            check_dir_contain_files_with_extensions(file_path)
            
        if file_name.endswith(extentions):
            raise Exception(f'Static test directory contains {file_name} file')


# Represents test for 'data' migration.
# Contains revision to be tested, it's previous revision, and callbacks that
# could be used to perform validation.
# MigrationValidationParamsGroup = namedtuple('MigrationData', [
#     'rev_base', 'rev_head', 'on_init', 'on_upgrade', 'on_downgrade'
# ])


# def load_migration_as_module(file: str):
#     """
#     Allows to import alembic migration as a module.
#     """
#     return importlib.machinery.SourceFileLoader(
#         file,
#         os.path.join(PROJECT_PATH, 'alembic', 'versions', file)
#     ).load_module()


# def make_validation_params_groups(
#         *migrations
# ) -> List[MigrationValidationParamsGroup]:
#     """
#     Creates objects that describe test for data migrations.
#     See examples in tests/data_migrations/migration_*.py.
#     """
#     data = []
#     for migration in migrations:

#         # Ensure migration has all required params
#         for required_param in ['rev_base', 'rev_head']:
#             if not hasattr(migration, required_param):
#                 raise RuntimeError(
#                     '{param} not specified for {migration}'.format(
#                         param=required_param,
#                         migration=migration.__name__
#                     )
#                 )

#         # Set up callbacks
#         callbacks = defaultdict(lambda: lambda *args, **kwargs: None)
#         for callback in ['on_init', 'on_upgrade', 'on_downgrade']:
#             if hasattr(migration, callback):
#                 callbacks[callback] = getattr(migration, callback)

#         data.append(
#             MigrationValidationParamsGroup(
#                 rev_base=migration.rev_base,
#                 rev_head=migration.rev_head,
#                 on_init=callbacks['on_init'],
#                 on_upgrade=callbacks['on_upgrade'],
#                 on_downgrade=callbacks['on_downgrade']
#             )
#         )

#     return data
