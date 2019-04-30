import psycopg2
import re


HOST = 'whatbot.ciquzj8l3yd7.ap-southeast-2.rds.amazonaws.com'
USERNAME = 'whatbot'
PASSWORD='12345678'
DATABASE = "postgres"
PORT = '5432'


class DataBaseManager:
    def __init__(self, host=HOST, port=PORT, database_name=DATABASE):
        self.host, self.port, self.database_name = host, port, database_name

    def connect_database(self):
        """Manages all database connection and autocommits

        :return: PostgreSQL connection object
        :rtype: connection object
        :return: PostgreSQL cursor
        :rtype: cursor object
        """
        connection = psycopg2.connect(database=self.database_name,
                                      user=USERNAME,
                                      password=PASSWORD,
                                      host=self.host,
                                      port=str(self.port))
        connection.set_session(autocommit=True)
        cursor = connection.cursor()
        return connection, cursor

    def disconnect_database(self, connection, cursor):
        """Manages all disconnection from database. Resets connection and cursor to None

        :return: None
        """
        cursor.close()
        connection.close()

    def execute_query(self, query, *args):
        """Used to execute query with the query string given and the arguments used for that
        query. Arguments are given through *args so we can use self.cursor.execute to sanitize
        the query and prevent SQL injection attacks.

        :param query: query string
        :type: str
        :param args: tuple of arguments that goes into query string in a tuple. This field is optional.
        :type: tuple
        :return: result of query
        :rtype: list or str
        """
        result = None
        try:
            connection, cursor = self.connect_database()
            if args:
                cursor.execute(query, (args[0]))
            else:
                cursor.execute(query)
            regex = re.compile(r'SELECT', re.IGNORECASE)
            result = cursor.fetchall() if regex.search(query) else "execute successfully"
        except (Exception, psycopg2.Error) as e:
            print(str(e))
        finally:
            self.disconnect_database(connection, cursor)
        return result


