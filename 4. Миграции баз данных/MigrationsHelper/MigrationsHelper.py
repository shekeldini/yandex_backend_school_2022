import os
import subprocess
from types import SimpleNamespace

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

from migrations.python.config import DefaultSettings

if "GITLAB_RUN" in os.environ.keys():
    db_host = "postgres"
else:
    db_host = "localhost"

db_string = DefaultSettings().database_uri
db = create_engine(db_string)


def update(migrations_count):
    if os.environ["SDB_TRACK"] == "java":
        update_java(str(migrations_count))
    else:
        update_python(str(migrations_count))


def rollback(migrations_count):
    if os.environ["SDB_TRACK"] == "java":
        rollback_java(str(migrations_count))
    else:
        rollback_python(str(migrations_count))


def make_alembic_config():
    cmd_opts = SimpleNamespace(config="alembic.ini", pg_url=db_string, name="alembic", raiseerr=False, x=None)
    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)
    config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)
    return config


def update_python(migrations_count):
    old_cwd = os.getcwd()
    os.chdir(os.path.join("migrations", "python"))
    try:
        command.upgrade(make_alembic_config(), f"+{migrations_count}")
    finally:
        os.chdir(old_cwd)


def rollback_python(migrations_count):
    old_cwd = os.getcwd()
    os.chdir(os.path.join("migrations", "python"))
    try:
        command.downgrade(make_alembic_config(), f"-{migrations_count}")
    finally:
        os.chdir(old_cwd)


def update_java(migrations_count):
    p = subprocess.Popen(["liquibase", "update-count", migrations_count], cwd="migrations/java")
    p.wait()


def rollback_java(migrations_count):
    p = subprocess.Popen(["liquibase", "rollback-count", migrations_count], cwd="migrations/java")
    p.wait()
