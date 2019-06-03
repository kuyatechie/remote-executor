import psycopg2
import os
from datetime import datetime

DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
DATABASE_NAME = os.getenv("DATABASE_NAME", "taskdb")
DATABASE_TABLE_NAME = os.getenv("DATABASE_TABLE_NAME", "task_task")
DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")


class DatabaseConnector:
    __instance = None

    def __new__(cls):
        if DatabaseConnector.__instance is None:
            DatabaseConnector.__instance = object.__new__(cls)
        return DatabaseConnector.__instance

    def __init__(self):
        self.connection = psycopg2.connect(user = DATABASE_USER,
                                           password=DATABASE_PASSWORD,
                                           host=DATABASE_HOSTNAME,
                                           port=DATABASE_PORT,
                                           database=DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def get_task_entry(self, uid):
        query = "select * from {} where uid = %s".format(DATABASE_TABLE_NAME)
        self.cursor.execute(query, (uid,))
        return self.cursor.fetchone()

    def update_task_retcode(self, uid, value):
        query = "update {} set {} = %s where uid = %s".format(DATABASE_TABLE_NAME, 'retcode')
        self.cursor.execute(query, (value, uid))
        self.connection.commit()

    def update_task_diskspace_before(self, uid, value):
        query = "update {} set {} = %s where uid = %s".format(DATABASE_TABLE_NAME, 'diskspace_before')
        self.cursor.execute(query, (value, uid))
        self.connection.commit()

    def update_task_diskspace_after(self, uid, value):
        query = "update {} set {} = %s where uid = %s".format(DATABASE_TABLE_NAME, 'diskspace_after')
        self.cursor.execute(query, (value, uid))
        self.connection.commit()

    def update_task_start_time(self, uid):
        query = "update {} set {} = %s where uid = %s".format(DATABASE_TABLE_NAME, 'started')
        self.cursor.execute(query, (datetime.today(), uid))
        self.connection.commit()

    def update_task_finish_time(self, uid):
        query = "update {} set {} = %s where uid = %s".format(DATABASE_TABLE_NAME, 'finished')
        self.cursor.execute(query, (datetime.today(), uid))
        self.connection.commit()
