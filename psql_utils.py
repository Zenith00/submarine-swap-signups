import psycopg2


def database_exists(cursor, name):
    cursor.execute(f"SELECT COUNT(*) = 0 FROM pg_catalog.pg_database WHERE datname = '{name}'")
    not_exists_row = cursor.fetchone()
    not_exists = not_exists_row[0]
    return not not_exists


def table_exists(con, table_str):
    cur = con.cursor()
    cur.execute(f"select exists(select relname from pg_class where relname='{table_str}')")
    exists = cur.fetchone()[0]
    cur.close()

    return exists


def get_table_col_names(con, table_str):
    col_names = []
    cur = con.cursor()
    cur.execute(f"select * from {table_str} LIMIT 0")
    for desc in cur.description:
        col_names.append(desc[0])
    cur.close()

    return col_names