import mysql.connector
import os


class DatabaseConnectivity:
    def __init__(self):
        self.config = {
            "host": os.getenv('DATABASE_HOST'),
            "user": os.getenv('DATABASE_USER'),
            "password": os.getenv('DATABASE_PASSWORD'),
            "database": os.getenv('DATABASE_NAME')
        }

    def get_connection(self):
        return mysql.connector.connect(**self.config)