import sqlite3
from sqlite3 import Error


def init_db(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS info
            (
                datetime TEXT,
                sensor TEXT,
                value INT
            )
        """
        )
    except Error as e:
        print(e)

    return conn


def add_data_point(conn, datetime, sensor, value):
    sql = """
            INSERT INTO info(datetime, sensor, value)
            VALUES(?,?,?)
            """
    cur = conn.cursor()
    cur.execute(sql, [datetime, sensor, value])
    conn.commit()
    return cur.lastrowid


def list_data_points(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT datetime, sensor, value
        FROM info ORDER BY datetime
    """
    )

    rows = cur.fetchall()
    return [
        {"created": datetime.replace("T", " ") + ":00", "name": sensor, "value": value}
        for datetime, sensor, value in rows
    ]
