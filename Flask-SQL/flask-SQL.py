###https://pusher.com/channels/pricing###
###https://pusher.com/channels/pricing###
###https://pusher.com/channels/pricing###
###https://pusher.com/channels/pricing###
###https://pusher.com/channels/pricing###

from flask import Flask, render_template, url_for, flash, request
from forms import *  # Mark the files containing folder as "source root" to avoid errors
from time import sleep
from threading import Thread
from flask import jsonify
import db
#import gps
import psycopg2
import os
import pusher
import pusher
SQL_list = []
data = []

def connection():
    connection = psycopg2.connect(user=db.user(),
                                    password=db.password(),
                                    host=db.host(),
                                    port=db.port(),
                                    database=db.dbName())
    return connection



pusher_client = pusher.Pusher(
  app_id='778793',
  key='4080a6dec8c62a9463de',
  secret='dfa02fca776126003da6',
  cluster='eu',
  ssl=True
)

#pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})


def get_DB_Data():
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM coordinates WHERE coordinates.bike_id NOT IN (SELECT bike_id FROM (SELECT DISTINCT ON (x, y) * FROM coordinates) AS dup)")
        cursor.execute("SELECT * FROM coordinates")
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
#def update():
#    print(gps.get())
#    gpsData = gps.get()
#    con = connection()
#    cursor = con.cursor()
#    cursor.execute("UPDATE coordinates SET x = {}, y = {} WHERE bike_id = {};".format(gpsData['x'],gpsData['y'],gpsData['bike_id']))
#    con.commit()
#update()
pusher_client.trigger(u'my-channel', u'my-event',get_DB_Data())
def get_table_data():
    for row in get_DB_Data():
        a = {'bike_id': row[3], 'name': row[0], 'x': row[1], 'y': row[2]}
        SQL_list.append(a)

def map_data():
    data.clear()
    for row in get_DB_Data():
        a = {'Primary_id': int(row[3]), 'name': row[0], 'x': float(row[1]), 'y': float(row[2])}
        data.append(a)
    return data

get_table_data()
map_data()

app = Flask(__name__)
app.config['SECRET_KEY'] = '123434211234342'  # This has to be here for "form.validate_on_submit()" to work
app.jinja_env.globals.update(map_data=map_data)
@app.route("/data")  # This is the data page

def home():
    return render_template('home.html', posts=SQL_list, title='Data page')  # The render_template by default goes to the folder called 'templates' and finds your document

@app.route("/pusher")
def pusher():
    return render_template('pusher.html', title='Pusher')

@app.route("/")  # To have two different routes lead to the same place have them on top of each other before the function
@app.route("/home")  # This is the home page
def about():
    return render_template('about.html', title='Home page')


@app.route("/map", methods=['GET', 'POST'])
def map():
    form = positionDataForm()
    # This try will take the data entered into the table on HTML and send it to the SQL server
    # If an except is not used an error will occur because it doesn't like the type of decimal field in WT-forms
    if form.is_submitted():
        con = connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO coordinates VALUES('{}', {}, {});".format(form.nameData.data, form.xData.data, form.yData.data))
        con.commit()
        map_data()  # Called to update the data makers on the map
    return render_template('map.html', title='Map', form=form, posts=data)

@app.route("/test")
def test():
    data.clear()
    for row in get_DB_Data():
        a = {'Primary_id': int(row[3]), 'name': row[0], 'x': float(row[1]), 'y': float(row[2])}
        data.append(a)
    return jsonify(data)


if __name__ == '__main__':  # Allows to run the page by running the script in cmd
    app.run(debug=True)
