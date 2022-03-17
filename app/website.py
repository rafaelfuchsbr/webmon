import requests
import logger
import re
from dbconnection import DBConnection 
from checkentry import CheckEntry

logger = logger.getLogger('website')

class Website():
    ERROR_HTTP_STATUS_THRESHOLD = 400; #HTTP status code to define if website is good or not

    def __init__(self, **atts):
        """
        Populate the object based on the given named parameters.
        """
        self.id = atts['id'] if 'id' in atts else None
        self.name = atts['name'] if 'name' in atts else None
        self.url = atts['url'] if 'url' in atts else None
        self.regex = atts['regex'] if 'regex' in atts else None
        self.status = atts['status'] if 'status' in atts else None
        self.timestamp = atts['timestamp'] if 'timestamp' in atts else None
        self.dbConn = None

        if self.id:
            self.load()

    def matchRegex(self, content):
        """
        Match the content of the HTTP GET request to check the website availability.
        If there is no regex, we will return true so we don't fail the availability because of this.
        """
        if self.regex:
            if not re.search(self.regex, content):
                return False
        return True

    def getCurrentAvailability(self):
        """
        It will make a HTTP request to the website URL and check the HTTP status code and if the
        content matches the regex for the website.
        It will update website status accordingly.
        _ regex not match or http status >= 400 --> unavailable
        - regex match and http satus < --> active
        """
        logger.info(f"Checking availability of website: id[{self.id}],name[{self.name}], url[{self.url}], regex[{self.regex}]")

        response = requests.get(url=self.url)
        responseMS = int(round(response.elapsed.total_seconds()*1000,0))
        regexMatch = self.matchRegex(response.text)
        entry = CheckEntry(website_id=self.id, http_status=response.status_code, response_time=responseMS, regex=self.regex, regex_match=regexMatch)
        logger.info(f"Availability of website: id[{self.id}],name[{self.name}], url[{self.url}] --> response_time={entry.response_time}ms, https_status={entry.http_status}")
        if entry.http_status >= self.ERROR_HTTP_STATUS_THRESHOLD or not regexMatch:
            self.status = 'unavailable'
        else:
            self.status = 'active'
        self.save(True)
        return entry

    def load(self, exists=False):
        """
        Load the website data from the database based on the ID.
        It's also used to check if the website already exists in the database.
        Return the website object.
        """
        sql = "select website_id, name, url, regex, status, timestamp from website where website_id = %(id)s"
        logger.debug(f"SQL statement to retrieve website: {sql}")

        conn = DBConnection()
        cursor = conn.getCursor()

        try:
            cursor.execute(sql, self.__dict__)
        except Exception as e:
            logger.error(f"Exception while running SQL [{sql}]", e)
            raise

        row = cursor.fetchone()
        if not row:
            logger.warning(f"Website with ID [{self.id}] not found.")
            conn.close()
            return False

        if exists:
            logger.info("Checking if website exists int the database - not populating the object again.")
            return True

        logger.debug(f"Website with ID [{self.id}] found, populating object.")
        self.id = row['website_id']
        self.name = row['name']
        self.url = row['url']
        self.regex = row['regex']
        self.status = row['status']
        self.timestamp = row['timestamp']

        conn.close()

        return self

    def delete(self):
        """
        Delete the website from the database.
        """
        sql = "delete from website where website_id=%(id)s"
        logger.debug(f"SQL statement to delete website: {sql}")
        conn = DBConnection()
        conn.getCursor().execute(sql, self.__dict__)
        conn.commit()
        self.__dict__ = {}
        conn.close()


    def save(self,forceUpdate=False):
        """
        Save the website obejct into the database.
        Call 'load' method to check if website already exists:
        - if yes, use update statement
        - if no, use insert statement
        Get the new ID back when inserting a new website.
        """
        if forceUpdate or self.load(exists=True):
            logger.debug(f"Website with ID [{self.id}] found, saving chnages with update statement.")
            sql = ( "update website set "
                    "name = %(name)s, "
                    "url = %(url)s, "
                    "regex = %(regex)s, "
                    "status = %(status)s "
                    "where website_id = %(id)s "
                    "RETURNING website_id "
                )
        else:
            logger.debug(f"Website with ID [{self.id}] not found, using insert statement.")
            sql = "insert into website(name, url, regex, status) values (%(name)s, %(url)s, %(regex)s, %(status)s) RETURNING website_id"

        logger.debug(f"SQL statement to save website object: {sql}")
        conn = DBConnection()
        cursor = conn.getCursor()
        cursor.execute(sql, self.__dict__)
        self.id = cursor.fetchone()[0]
        logger.debug(f"Generated website id: {self.id}")
        conn.commit()
        conn.close()

        return self
