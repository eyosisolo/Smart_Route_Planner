from database import get_connection


def create_locations_table():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
        """)

        connection.commit()

        # Check whether the address column exists.
        cursor.execute("PRAGMA table_info(locations)")

        columns = cursor.fetchall()

        column_names = [
            column["name"]
            for column in columns
        ]

        # Upgrade an older database that did not have
        # the address column.
        if "address" not in column_names:

            cursor.execute("""
                ALTER TABLE locations
                ADD COLUMN address TEXT NOT NULL DEFAULT ''
            """)

            connection.commit()

    finally:

        connection.close()


def add_location(
    name,
    address,
    latitude,
    longitude
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO locations(
                name,
                address,
                latitude,
                longitude
            )
            VALUES (?, ?, ?, ?)
        """, (
            name,
            address,
            latitude,
            longitude
        ))

        connection.commit()

    finally:

        connection.close()


def get_all_locations():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                address,
                latitude,
                longitude
            FROM locations
            ORDER BY id ASC
        """)

        rows = cursor.fetchall()

        # Convert SQLite Row objects into
        # normal Python dictionaries.
        locations = [
            dict(row)
            for row in rows
        ]

        return locations

    finally:

        connection.close()