import psycopg2
SQL_list = []
try:
    connection = psycopg2.connect(user="postgres",
                                  password="qw1212qw",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="baj")
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from games"
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from mobile table using cursor.fetchall")
    games = cursor.fetchall()

    print("Print each row and it's columns values", "\n")
    for row in games:
        print("game_id = ", row[0])  # Row (vertical) column 0
        print("game_dt = ", row[1])  # Row (vertical) column 1
        print("home_team_id", row[2])  # Row (vertical) column 2
        print("guest_team_id  = ", row[3], "\n")  # Row (vertical) column 3
        a = {'game_id': row[0], 'game_dt': row[1], 'home_team_id': row[2], 'guest_team_id': row[3]}
        SQL_list.append(a)
    print(SQL_list)
except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")