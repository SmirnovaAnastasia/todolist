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





# def update_single_record():
#     conn = None
#     cursor = None
#     try:
#         conn = psycopg2.connect(
#             dbname="todolist",
#             user="postgres",
#             password="mava",
#             host="localhost"
#         )
#         cursor = conn.cursor()
#
#         update_query = "UPDATE mobile SET price = %s WHERE id = %s"
#         cursor.execute(update_query, (970, 3))
#
#         conn.commit()  # Фиксируем изменения
#         print(
#             f"{cursor.rowcount} запись успешно обновлена")  # rowcount показывает количество изменённых строк [citation:4]
#
#     except (Exception, psycopg2.Error) as error:
#         print("Ошибка при обновлении:", error)
#     finally:
#         if conn:
#             cursor.close()
#             conn.close()
#             print("Соединение с PostgreSQL закрыто")


# def update_multiple_records(date, tasks_list):
#     cursor = None
#
#     conn = psycopg2.connect(
#             dbname="todolist",
#             user="postgres",
#             password="mava",
#             host="localhost"
#     )
#
#     try:
#         cursor = conn.cursor()
#
#         # Используем INSERT с ON CONFLICT для обновления при существовании даты
#         query = """
#         INSERT INTO tasks (date_, doings)
#         VALUES (%s, %s)
#         ON CONFLICT (date_)
#         DO UPDATE SET doings = EXCLUDED.doings;
#         """
#
#         cursor.execute(query, (date, json.dumps(tasks_list)))
#         conn.commit()
#         print(f"✅ Данные для {date} успешно обновлены")
#
#     except Exception as e:
#         print(f"❌ Ошибка: {e}")
#         conn.rollback()
#     finally:
#         cursor.close()
#         conn.close()

