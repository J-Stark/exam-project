import psycopg2
import db
import json


def connection():
    connection = psycopg2.connect(user=db.user(),
                                    password=db.password(),
                                    host=db.host(),
                                    port=db.port(),
                                    database=db.dbName())
    return connection


def get_json_DB():
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM coordinates WHERE coordinates.bike_id NOT IN (SELECT bike_id FROM (SELECT DISTINCT ON (x, y) * FROM coordinates) AS dup)")
        cursor.execute("SELECT bike_id, row_to_json((SELECT d FROM (SELECT x, y) d)) AS bikes FROM coordinates")
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

def main():
    dump = get_json_DB()
    print (dump[1][1]['x'])

if __name__ == '__main__':  # Allows to run the page by running the script in cmd
    main()
