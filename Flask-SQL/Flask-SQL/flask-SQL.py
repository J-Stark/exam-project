from flask import Flask, render_template, jsonify
from forms import *  # Mark the files containing folder as "source root" to avoid errors
import db
#import gps
import psycopg2

def connection():
    connection = psycopg2.connect(user=db.user(),
                                    password=db.password(),
                                    host=db.host(),
                                    port=db.port(),
                                    database=db.dbName())
    return connection


def get_DB(query):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM coordinates WHERE coordinates.bike_id NOT IN (SELECT bike_id FROM (SELECT DISTINCT ON (x, y) * FROM coordinates) AS dup)")
        cursor.execute(query)
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


# def update():
#    print(gps.get())
#    gpsData = gps.get()
#    con = connection()
#    cursor = con.cursor()
#    cursor.execute("UPDATE coordinates SET x = {}, y = {} WHERE bike_id = {};".format(gpsData['x'],gpsData['y'],gpsData['bike_id']))
#    con.commit()
# update()


def get_table_data():
    SQL_list = []
    for row in get_DB("SELECT * FROM coordinates"):
        a = {'bike_id': row[3], 'name': row[0], 'x': row[1], 'y': row[2], 'time': row[4]}
        SQL_list.append(a)
    return SQL_list


app = Flask(__name__)
app.config['SECRET_KEY'] = '123434211234342'  # Forms


@app.route("/data")  # This is the data page
def dataPage():
    return render_template('data.html', posts=get_table_data(), title='Data page')


@app.route("/")  # Regular page leads to homepage too.
@app.route("/home")  # This is the home page
def home():
    return render_template('home.html', title='Home page')


@app.route("/map", methods=['GET', 'POST'])
def map():
    form = positionDataForm()
    if form.is_submitted():
        con = connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO coordinates VALUES('{}', {}, {});".format(form.nameData.data, form.xData.data, form.yData.data))
        con.commit()
    return render_template('map.html', title='Map', form=form)


@app.route("/update")
def update():
    jsonStr = get_DB("SELECT bike_id, row_to_json((SELECT d FROM (SELECT x, y) d)) AS bikes FROM coordinates")
    return jsonify(bikes=jsonStr)


if __name__ == '__main__':  # Allows to run server through terminal.
    app.run(debug=True)
