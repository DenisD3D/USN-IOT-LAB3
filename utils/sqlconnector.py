import os

import psycopg2
from dotenv import load_dotenv


class SQLConnector:
    def __init__(self, database: str, host: str, user: str, password: str, port: str):
        self.connection = psycopg2.connect(database=database, host=host, user=user, password=password, port=port)

    def upload_temperature(self, temperature: float):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO public.temperatures (temperature, created_at) VALUES (%s, CURRENT_TIMESTAMP)", (temperature,))
        self.connection.commit()
        cursor.close()

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    load_dotenv()

    sql = SQLConnector(os.getenv("SQL_DATABASE"), os.getenv("SQL_HOST"), os.getenv("SQL_USER"), os.getenv("SQL_PASSWORD"), os.getenv("SQL_PORT"))
    sql.upload_temperature(20)
    sql.close()
