from flask import Flask, render_template, jsonify, redirect, flash
from forms import *  # Mark the files containing folder as "source root" to avoid errors
import db
import gps
import psycopg2
from psycopg2._psycopg import IntegrityError
import datetime
from tabulate import tabulate
username = ""
rented = ""
DT = ""
user_list=[]
bikes_list=[]
loggedIn = False

def connection():
    connection = psycopg2.connect(user=db.user(),
                                    password=db.password(),
                                    host=db.host(),
                                    port=db.port(),
                                    database=db.dbName())

    connection.autocommit = True
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


def checkGPS():
    gpsData = gps.get()
    con = connection()
    cursor = con.cursor()
    for bike in gpsData:
        cursor.execute("UPDATE coordinates SET x = {}, y = {} WHERE bike_id = {};".format(bike['x'],bike['y'],bike['bike_id'])) # GOTTA ADD TIME LATER
        con.commit()


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
    return render_template('data.html', posts=get_table_data(), title='Data page', loggedIn = loggedIn)


@app.route("/")  # Regular page leads to homepage too.
@app.route("/home")  # This is the home page
def home():
    return render_template('home.html', title='Home page', loggedIn = loggedIn)


@app.route("/map", methods=['GET', 'POST'])
def map():
    form = positionDataForm()
    if form.is_submitted():
        con = connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO coordinates VALUES('{}', {}, {});".format(form.nameData.data, form.xData.data, form.yData.data))
        con.commit()
    return render_template('map.html', title='Map', form=form, loggedIn = loggedIn)


@app.route("/update")
def update():
    checkGPS()
    jsonStr = get_DB("SELECT bike_id, row_to_json((SELECT d FROM (SELECT x, y) d)) AS bikes FROM coordinates")
    return jsonify(bikes=jsonStr)


def check_if_availble(bike_id):
    global status_bike
    cursor=connection().cursor()
    asa= str("SELECT avaibility FROM coordinates WHERE bike_id='" + bike_id + "';")
    cursor.execute(asa)
    status_bike = cursor.fetchone()
    connection().close()


def check_if_rented():
    global status
    cursor=connection().cursor()
    asa = str("SELECT rented FROM users WHERE username='" + username + "';")
    cursor.execute(asa)
    status = cursor.fetchone()
    connection().close()

def check_if_credits():
    global yourcredits
    cursor=connection().cursor()
    asa = str("SELECT credits FROM users WHERE username='" + username + "';")
    cursor.execute(asa)
    yourcredits0 = cursor.fetchone()
    yourcredits=yourcredits0[0]
    connection().close()
    return yourcredits


def update_rented():
    global rented
    cursor=connection().cursor()
    cursor.execute("SELECT rented FROM users WHERE username='" + username + "';")
    status2 = cursor.fetchone()
    print(status2)
    if status2[0] == 0:
        rented = "None"
    if status2[0] == 1:
        rented = "1"
    if status2[0] == 2:
        rented = "2"
    if status2[0] == 3:
        rented = "3"
    connection().close()
    return rented


def update_credits():
    global credits
    cursor=connection().cursor()
    cursor.execute("SELECT credits FROM users WHERE username='"+ username + "';")
    credits0= cursor.fetchone()
    credits= credits0[0]
    return credits


def get_time():
    global DT
    DT = datetime.datetime.now()
    return DT


@app.route('/register', methods=['GET', 'POST'])
def post_userdata():
    form = usersDataForm()
    # This try will take the data entered into the table on HTML and send it to the SQL server
    if form.is_submitted():
        try:
            con = connection()
            cursor = con.cursor()
            cursor.execute("INSERT INTO users VALUES('{}','{}', 0, 0);".format(form.usernameData.data, form.passwordData.data))
            con.commit()
            flash('Thanks for registering!', 'success')
        except IntegrityError:
            con = connection()
            con.rollback()
            flash('ERROR! Username ({}) already exists.'.format(form.usernameData.data), 'error')

    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    global loggedIn
    loggedIn = False
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def get_userdata():
    form = usersDataForm()
    if form.is_submitted():
        global username
        username = form.usernameData.data
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '{}' AND pass = '{}';".format(form.usernameData.data, form.passwordData.data))
        status = cursor.fetchone()

        if status != None and username!="Admin":
            update_rented()
            global loggedIn
            loggedIn = True
            return redirect('/')

        else:
            flash('username or/and password incorrect')

    return render_template('login.html', form=form)

################################################################################## Don't change anything above this line

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    update_rented()
    get_time()
    update_credits()
    return render_template('user_profile.html', username=username, rented=rented, credits=credits), rented

@app.route('/return', methods=['GET','POST'])
def returnbike():
    check_if_rented()
    if status[0]!=0:
        conn1=connection()
        cur1=conn1.cursor()
        sql1="UPDATE users SET rented=0 WHERE username='" + username + "';"
        sql2= "UPDATE coordinates SET avaibility = 0 WHERE bike_id='" + rented + "';"
        sql3 = "SELECT rent_date FROM coordinates WHERE bike_id='" + rented + "';"
        sql4 = "UPDATE coordinates SET rent_date=NULL WHERE bike_id='" + rented + "';"
        cur1.execute(sql1)
        connection().commit()
        cur1.close()
        conn2 = connection()
        cur2= conn2.cursor()
        cur2.execute(sql2)
        connection().commit()
        cur2.close()
        conn3 = connection()
        cur3 = conn3.cursor()
        cur3.execute(sql3)
        date1 = cur3.fetchone()
        connection().commit()
        cur3.close()
        flash("You've returned the bike!")

        datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        conn4 = connection()
        cur4 = conn4.cursor()
        cur4.execute(sql4)
        date2= get_time()
        date1=str(date1[0])
        date2=str(date2)

        diff = datetime.datetime.strptime(date2, datetimeFormat) \
              - datetime.datetime.strptime(date1, datetimeFormat)
        minutes= int(round(diff.seconds/60))

        flash("You've rented it at: ")
        flash(date1)
        flash("You've returned it at: ")
        flash(date2)
        flash("Minutes:")
        flash(minutes)

        charge = 10 + 0.02*minutes
        flash("You've been charged:")
        flash(charge)

        credits_after_rent = credits - charge
        sql5= "UPDATE users SET credits={} WHERE username='{}'"
        conn5 = connection()
        cur5 = conn5.cursor()
        cur5.execute(sql5.format(credits_after_rent,username))
        connection().commit()
        cur2.close()


    else:
        flash("You don't have any bike rented!")

    return redirect('/user_profile')


@app.route('/rental', methods=['GET', 'POST'])
def rent_bike():
    check_if_rented()
    check_if_credits()
    if yourcredits < 20:
        flash("Not enough credits to rent a bike. Must be at least 20 dkk!")
        return render_template("user_profile.html", username=username, rented=rented, credits=credits)
    if status[0] != 0:
        flash("You already have bike rented!")
        return render_template("user_profile.html", username=username, rented=rented, credits=credits), rented
    return render_template("rentbike.html"), rented

@app.route('/bike1', methods=['GET','POST'])
def rent_bike1():
    check_if_availble('1')
    if status_bike[0] == 0:
        get_time()
        conn1 = connection()
        cur1 = conn1.cursor()
        sql1 = "UPDATE users SET rented=1 WHERE username='" + username + "';"
        sql2 = "UPDATE coordinates SET avaibility=1 WHERE bike_id='1';"
        #sql3 = "UPDATE bikes SET rent_date=" + datetime.datetime.now() + " WHERE bike_id='1'"
        sql3 = "UPDATE coordinates SET rent_date=now() WHERE bike_id='1'"
        cur1.execute(sql1)
        connection().commit()
        cur1.close()
        conn2 = connection()
        cur2 = conn2.cursor()
        cur2.execute(sql2)
        connection().commit()
        cur2.close()
        conn3 = connection()
        cur3 = conn3.cursor()
        cur3.execute(sql3)
        conn3.commit()
        cur3.close()

        flash("You've rented this bike! Enjoy!")
        return redirect('/user_profile')
    else:
        flash('Bike1 not availble :(')
    return render_template('rentbike.html', username=username, rented=rented), rented

@app.route('/bike2', methods=['GET','POST'])
def rent_bike2():
    check_if_availble('2')
    if status_bike[0] == 0:
        conn1 = connection()
        cur1 = conn1.cursor()
        sql1 = "UPDATE users SET rented=2 WHERE username='" + username + "';"
        sql2 = "UPDATE coordinates SET avaibility=1 WHERE bike_id='2';"
        sql3 = "UPDATE coordinates SET rent_date=now() WHERE bike_id='2'"
        cur1.execute(sql1)
        connection().commit()
        cur1.close()
        conn2 = connection()
        cur2 = conn2.cursor()
        cur2.execute(sql2)
        connection().commit()
        cur2.close()
        conn3 = connection()
        cur3 = conn3.cursor()
        cur3.execute(sql3)
        conn3.commit()
        cur3.close()
        flash("You've rented this bike! Enjoy!")
        return redirect('/user_profile')
    else:
        flash('Bike2 not availble :(')
    return render_template('rentbike.html', username=username, rented=rented), rented

@app.route('/bike3', methods=['GET','POST'])
def rent_bike3():
    check_if_availble('3')
    if status_bike[0] == 0:
        conn1 = connection()
        cur1 = conn1.cursor()
        sql1 = "UPDATE users SET rented=3 WHERE username='" + username + "';"
        sql2 = "UPDATE coordinates SET avaibility=1 WHERE bike_id='3';"
        sql3 = "UPDATE coordinates SET rent_date=now() WHERE bike_id='3'"
        cur1.execute(sql1)
        connection().commit()
        cur1.close()
        conn2 = connection()
        cur2 = conn2.cursor()
        cur2.execute(sql2)
        connection().commit()
        cur2.close()
        conn3 = connection()
        cur3 = conn3.cursor()
        cur3.execute(sql3)
        conn3.commit()
        cur3.close()
        flash("You've rented this bike! Enjoy!")
        return redirect('/user_profile')
    else:
        flash('Bike3 not availble :(')
    return render_template('rentbike.html', username=username, rented=rented), rented


@app.route('/credits', methods=['GET','POST'])
def add_credits():
    form = usersDataForm()
    if form.is_submitted():
        credits_to_add = form.creditsData.data
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT credits FROM users WHERE username='" + username + "';")
        credits_prev = cursor.fetchone()[0]
        credits_new = credits_to_add+credits_prev
        cursor.execute("UPDATE users SET credits={} WHERE username='{}'".format(credits_new, username))
        con.commit()
        flash("Your credits were added!")
    return render_template('credits.html', form=form)


@app.route('/admin', methods=['GET','POST'])
def admin_login():
    form = usersDataForm()
    cur = connection().cursor()
    cur.execute("SELECT pass from users WHERE username='Admin'")
    password = cur.fetchone()
    print(password)
    if form.is_submitted():
        if form.usernameData.data == 'Admin' and form.passwordData.data == password[0]:
            return redirect('/admin_page')
        else:
            flash("WRONG")
    return render_template('adminlogin.html', form=form)


@app.route('/admin_page', methods=['GET','POST'])
def admin_page():
    form = usersDataForm()
    if form.is_submitted():
        user = form.usernameData.data
        newcredits = form.creditsData.data
        cur = connection().cursor()
        cur.execute("UPDATE users SET credits={} WHERE username='{}'".format(newcredits, user))
        connection().commit()
        flash("You've changed this users credits")

    return render_template('adminpage.html', form=form)


@app.route('/admin_into_file', methods=['GET', 'POST'])
def into_file():
    date0 = datetime.datetime.now()
    date = date0.strftime('%y-%m-%d-%H-%M-%S')
    file_name = ("Data" + date + ".txt")
    bikes_list.clear()
    user_list.clear()
    con = connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM coordinates")
    bikes=cursor.fetchall()
    cursor.close()
    cursor=con.cursor()
    cursor.execute("SELECT * FROM users")
    users=cursor.fetchall()
    for row in bikes:
        a= {'bike_name': row[0], 'availblity': row[5], 'rent_date': row[4]}
        bikes_list.append(a)
    for row in users:
        a={'username': row[0], 'password': row[1],'rented': row[2], 'credits': row[3]}
        user_list.append(a)

        with open(file_name, "w+") as fOut:

            fOut.write(tabulate(bikes_list, headers="keys"))
            fOut.write(tabulate(user_list,  headers="keys"))

            fOut.close()



    flash("Data has been saved into a file")


    return redirect('/admin_page')


if __name__ == '__main__':  # Allows to run server through terminal.
    app.run(debug=True)
