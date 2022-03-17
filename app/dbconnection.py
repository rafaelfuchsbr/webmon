import psycopg2
import psycopg2.extras

import logger
import config

logger = logger.getLogger('dbconnection')
config = config.config()

class DBConnection():
    MAX_RETRY = 3

    def __init__(self):
        self.connect()
        self.cursor = None

    def getCursor(self):
        """
        Singletone like approach to get cursors.
        """
        if not self.conn:
            logger.debug("Connection to DB not established yet, getting one now.")
            self.connect()

        if not self.cursor:
            logger.debug("Cursor not set yet, getting a new one.")
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        else:
            logger.debug("DB and cursor were already defined, returning existing cursor.")
        return self.cursor

    def connect(self):
        """
        Get database connection. If trying to get a connection from the same object, it will act like a singletone.
        """
        while range(self.MAX_RETRY):
            try:
                logger.debug(f"Connecting to the database [host:{config.database.host}, port:{config.database.port}, db:{config.database.db}, user:{config.database.user}].")
                self.conn = psycopg2.connect(
                    host=config.database.host,
                    port=config.database.port,
                    sslmode="require",
                    connect_timeout=10,
                    database=config.database.db,
                    user=config.database.user,
                    password=config.database.password)
                logger.debug("Connected to the database.")
                return self.conn
            except Exception as e:
                logger.error("Error while connecting to the database", e)

        raise Exception("Could not connect to the database.")

    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            logger.error("Error while commiting to the database", e)
            return

        logger.debug("Database transaction commited.")

    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            logger.error("Error while closing the database", e)
            return
        finally:
            self.conn = None

        logger.debug("Database connection closed / released.")