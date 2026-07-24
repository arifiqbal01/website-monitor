from .connection import get_connection


def initialize_database() -> None:
    """
    Creates all database tables if they do not exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    #
    # Websites
    #
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS websites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    #
    # Generic monitoring results
    #
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monitor_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        website_id INTEGER NOT NULL,

        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        status TEXT NOT NULL,

        response_time REAL,

        http_code INTEGER,

        failure_type TEXT,

        failure_message TEXT,

        FOREIGN KEY (website_id)
            REFERENCES websites(id)
            ON DELETE CASCADE
    )
    """)

    #
    # WordPress-specific monitoring results
    #
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wordpress_results (

        monitor_result_id INTEGER PRIMARY KEY,

        wordpress_version TEXT,

        rest_api BOOLEAN,

        xmlrpc BOOLEAN,

        login_page BOOLEAN,

        database_error BOOLEAN,

        maintenance_mode BOOLEAN,

        FOREIGN KEY (monitor_result_id)
            REFERENCES monitor_results(id)
            ON DELETE CASCADE
    )
    """)

    connection.commit()
    connection.close()