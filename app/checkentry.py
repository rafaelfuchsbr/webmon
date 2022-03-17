import datetime
import yaml
import uuid

import logger
from dbconnection import DBConnection 

logger = logger.getLogger('checkentry')

class CheckEntry():

    def __init__(self, **atts):
        self.id = atts['id'] if 'id' in atts else str(uuid.uuid1())
        self.website_id = atts['website_id'] if 'website_id' in atts else None
        self.response_time = atts['response_time'] if 'response_time' in atts else None
        self.http_status = atts['http_status'] if 'http_status' in atts else None
        self.regex = atts['regex'] if 'regex' in atts else None
        self.regex_match = atts['regex_match'] if 'regex_match' in atts else None
        self.timestamp = atts['timestamp'] if 'timestamp' in atts else datetime.datetime.now()

    def getYaml(self):
        logger.debug(f"Returning YAML for check entry [id: {self.id}]")
        return yaml.dump(self.__dict__)

    def load(self):
        """
        Load the entry object from the database.
        Not being used right now, but may be used for future features.
        """
        sql = "select check_entry_id, website_id, response_time, http_status, regex, regex_match, timestamp from check_entry where check_entry_id = %(id)s"
        logger.debug(f"SQL statement to retrieve check entry: {sql}")

        conn = DBConnection()
        cursor = conn.getCursor()
        cursor.execute(sql, self.__dict__)
        row = cursor.fetchone()
        if not row:
            logger.warning(f"Check entry with ID [{self.id}] not found.")
            conn.close()
            return False

        logger.debug(f"Check entry with ID [{self.id}] found, populating object.")
        self.id = row['check_entry_id']
        self.website_id = row['website_id']
        self.response_time = row['response_time']
        self.http_status = row['http_status']
        self.regex = row['regex']
        self.regex_match = row['regex_match']
        self.timestamp = row['timestamp']

        conn.close()

        return True

    def save(self):
        """
        Simple save/insert for the check entry object.
        I don't expect to change these entries, so no update approach is available.
        """
        sql = "insert into check_entry(website_id, response_time, http_status, regex, regex_match) values (%(website_id)s, %(response_time)s, %(http_status)s, %(regex)s, %(regex_match)s) RETURNING check_entry_id, timestamp"
        logger.debug(f"SQL statement to save check entry object: {sql}")

        conn = DBConnection()
        cursor = conn.getCursor()
        cursor.execute(sql, self.__dict__)
        fields = cursor.fetchone()
        self.id = fields[0]
        self.timestamp = fields[1]
        logger.debug(f"Generated check entry id: {self.id}")
        conn.commit()
        conn.close()
