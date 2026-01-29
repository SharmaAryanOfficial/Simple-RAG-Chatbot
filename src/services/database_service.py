from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
from typing import Optional

class DatabaseManager:
    """
    """
    def __init__(self):
        """
        """
        self.pool: Optional[ConnectionPool] = None

    def initialize(self, Connection_string: str):
        """

        """
        self.pool = ConnectionPool(
            conninfo=Connection_string,
            min_size=20,
            kwargs={"autocommit": True, "prepare_threshold": 0}
            )

        #setuo the checkpoint saver
        with self.pool.connection() as conn:
            saver = PostgresSaver(conn)
            saver.setup()

    def close(self):
        """
        """
        if self.pool:
            self.pool.close()

    def get_saver(self) -> PostgresSaver:
        """
        """
        if not self.pool:
            raise ValueError("Connection pool is not initialized.")

        return PostgresSaver(self.pool)

db_manager = DatabaseManager()