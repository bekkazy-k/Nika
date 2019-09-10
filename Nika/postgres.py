# https://pynative.com/psycopg2-python-postgresql-connection-pooling/
# https://toster.ru/q/638535 - Реализовать по данному примеру
import psycopg2
from psycopg2 import pool
import datetime
from Nika import colorprint as p


class PostgresConn:
    def __init__(self, user, password, host, port, database):
        self.__pool = None
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        self.connect()

    def connect(self):
        try:
            self.__pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=self.user, password=self.password,
                                                             host=self.host, port=self.port, database=self.database)
            if self.__pool:
                p.pr('##', 'Postgres connection pool created successfully', c='b,c')
            else:
                raise ConnectionRefusedError("error trying to open connection pool")
        except (Exception, psycopg2.DatabaseError) as error:
            raise ConnectionError(f'An error while trying to establish a connection with Postgres. '
                                  f'Error text: {str(error)}')

    def get_conn(self):
        if self.__pool:
            return self.__pool.getconn()
        else:
            raise ConnectionRefusedError("Connection pool is empty")

    def close_conn(self, connection):
        if self.__pool:
            self.__pool.putconn(connection)
        else:
            raise ConnectionRefusedError("Connection pool is empty")

    def disconnect(self):
        if self.__pool:
            self.__pool.closeall
        print("PostgreSQL connection pool is closed")

    def execute(self):
        # connection = self.get_conn()
        # cursor = connection.cursor()
        # cursor.execute("select * FROM vbiuser.mobile order by 1 asc")
        # mobile_records = cursor.fetchmany(size=100)
        #
        # for row in mobile_records:
        #     print(row)
        #
        # cursor.close()
        #
        # self.close_conn(connection)
        pass

    def insert(self, table, cols: list, rows: list):
        connection = None
        try:
            query_cols = ""
            query_vals = ""
            for i in cols:
                query_cols += i+", "
                query_vals += "%s,"
            query = f'INSERT INTO {table} ({query_cols[:-2]}) VALUES ({query_vals[:-1]})'

            connection = self.get_conn()
            if connection:
                cursor = connection.cursor()
                cursor.execute(query, rows)
                connection.commit()
                # count = cursor.rowcount
                # print(count, f'Record inserted successfully into {table} table')
            self.close_conn(connection)

        except (Exception, psycopg2.Error) as error:
            if connection:
                print(f'Failed to insert record into mobile table', error)
                raise ConnectionError(f'Failed to insert record into mobile table. Error text: {str(error)}')
            else:
                raise ConnectionError(f'Unknown error: {str(error)}')

    def new_log(self, src_project_name, log_type, log_text):
        self.insert('vbiuser.logs', ['created_at', 'updated_at', 'source', 'log_type', 'log_text'],
                    [datetime.datetime.now(), datetime.datetime.now(), src_project_name, log_type, log_text])



