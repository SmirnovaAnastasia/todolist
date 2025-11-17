import psycopg2
import json
import configparser
from psycopg2 import Error

def read_config():
    config = configparser.ConfigParser()

    config.read('config.ini')

    dbname_file = config.get('Database', 'dbname')
    user_file = config.get('Database', 'user')
    password_file = config.get('Database', 'password')
    host_file = config.get('Database', 'host')

    config_values = {
        'dbname': dbname_file,
        'user': user_file,
        'password': password_file,
        'host': host_file
    }

    return config_values

def get_all_tasks():

    config_values = read_config()
    with psycopg2.connect(
            dbname = config_values['dbname'],
            user = config_values['user'],
            password =config_values['password'],
            host = config_values['host']
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks ORDER BY date_")

            all_rows = cursor.fetchall()
            tasks_data = all_rows

            return tasks_data

def overwrite_from_all_rows(tasks_data):
    cursor = None

    config_values = read_config()
    conn = psycopg2.connect(
            dbname = config_values['dbname'],
            user = config_values['user'],
            password =config_values['password'],
            host = config_values['host']
    )

    try:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks;")

        for row in tasks_data:
            date_ = row[0]
            doings = row[1]

            doings = json.dumps(doings)

            cursor.execute(
                "INSERT INTO tasks (date_, doings) VALUES (%s, %s);",
                (date_, doings)
            )

        conn.commit()

    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
