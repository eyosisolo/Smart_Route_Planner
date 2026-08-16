from database import get_connection


# ============================================================
# LOCATIONS TABLE
# ============================================================

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

        # Upgrade an older database if necessary.
        if "address" not in column_names:

            cursor.execute("""
                ALTER TABLE locations
                ADD COLUMN address TEXT NOT NULL DEFAULT ''
            """)

            connection.commit()

    finally:

        connection.close()


# ============================================================
# DRIVER START TABLE
# ============================================================

def create_driver_start_table():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS driver_start(
                id INTEGER PRIMARY KEY,
                address TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
        """)

        connection.commit()

    finally:

        connection.close()


# ============================================================
# ADD LOCATION
# ============================================================

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


# ============================================================
# GET ALL LOCATIONS
# ============================================================

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

        return [
            dict(row)
            for row in rows
        ]

    finally:

        connection.close()


# ============================================================
# GET SELECTED LOCATIONS
# ============================================================

def get_locations_by_ids(location_ids):

    if not location_ids:

        return []

    connection = get_connection()

    try:

        cursor = connection.cursor()

        placeholders = ",".join(
            "?" for _ in location_ids
        )

        query = f"""
            SELECT
                id,
                name,
                address,
                latitude,
                longitude
            FROM locations
            WHERE id IN ({placeholders})
            ORDER BY id ASC
        """

        cursor.execute(
            query,
            location_ids
        )

        rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:

        connection.close()


# ============================================================
# DELETE LOCATION
# ============================================================

def delete_location(location_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM locations
            WHERE id = ?
            """,
            (location_id,)
        )

        connection.commit()

    finally:

        connection.close()


# ============================================================
# SAVE / UPDATE DRIVER START
# ============================================================

def save_driver_start(
    address,
    latitude,
    longitude
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # Because id is always 1, there can only
        # be one current driver starting location.
        cursor.execute("""
            INSERT INTO driver_start(
                id,
                address,
                latitude,
                longitude
            )
            VALUES (?, ?, ?, ?)

            ON CONFLICT(id)
            DO UPDATE SET
                address = excluded.address,
                latitude = excluded.latitude,
                longitude = excluded.longitude
        """, (
            1,
            address,
            latitude,
            longitude
        ))

        connection.commit()

    finally:

        connection.close()


# ============================================================
# GET DRIVER START
# ============================================================

def get_driver_start():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                address,
                latitude,
                longitude
            FROM driver_start
            WHERE id = 1
        """)

        row = cursor.fetchone()

        if row is None:

            return None

        return dict(row)

    finally:

        connection.close()