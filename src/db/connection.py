from duckdb import DuckDBPyConnection, connect
from os import getenv


POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_HOST = getenv("POSTGRES_HOST")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
R2_BUCKET = getenv("R2_BUCKET")

R2_ACCESS_KEY_ID = getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = getenv("R2_SECRET_ACCESS_KEY")
R2_ACCOUNT_ID = getenv("R2_ACCOUNT_ID")


def get_db():
    return connect()


def attach_ducklake(connection: DuckDBPyConnection):
    connection.execute(
        f"CREATE OR REPLACE SECRET r2 (TYPE R2, KEY_ID '{R2_ACCESS_KEY_ID}', SECRET '{R2_SECRET_ACCESS_KEY}', ACCOUNT_ID '{R2_ACCOUNT_ID}');"
    )
    connection.execute("INSTALL ducklake; LOAD ducklake;")
    connection.query(
        f"ATTACH 'ducklake:postgres:dbname={POSTGRES_DB} host={POSTGRES_HOST} user={POSTGRES_USER} password={POSTGRES_PASSWORD} sslmode=require' AS ducklake (DATA_PATH 'r2://{R2_BUCKET}/data');"
    )
