from database import get_connection


def create_locations_table():

    connection = get_connection()
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
    connection.close()


def add_location(name, address, latitude, longitude):

    connection = get_connection()
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
    connection.close()


def get_all_locations():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            address,
            latitude,
            longitude
        FROM locations
        ORDER BY id
    """)

    locations = cursor.fetchall()

    connection.close()

    return locations