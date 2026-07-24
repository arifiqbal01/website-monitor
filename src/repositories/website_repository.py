from src.database.connection import get_connection
from src.domain.model import Website


class WebsiteRepository:

    def get(self, website: Website) -> int | None:
        """
        Returns the database ID for a website.

        Does not create a new record.
        """

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM websites
            WHERE url = ?
            """,
            (website.url,),
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return row["id"]

    def get_or_create(self, website: Website) -> int:
        """
        Returns the database ID for a website.
        Creates it if it doesn't already exist.
        """

        website_id = self.get(website)

        if website_id is not None:
            return website_id

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO websites (url, type)
            VALUES (?, ?)
            """,
            (
                website.url,
                website.type.value,
            ),
        )

        connection.commit()

        website_id = cursor.lastrowid

        connection.close()

        return website_id