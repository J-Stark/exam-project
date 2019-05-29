from flask import Flask, flash
from psycopg2._psycopg import IntegrityError
from forms import *
from flask import redirect, render_template
import datetime
import psycopg2
from tabulate import tabulate

username = ""
rented = ""
DT = ""
user_list=[]
bikes_list=[]



def check_if_availble(bike_name):
    global status_bike
    cursor=connection().cursor()
    asa= str("SELECT avaibility FROM bikes WHERE bike_name='" + bike_name + "';")
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
    if status2[0] == 0:
        rented = "None"
    if status2[0] == 1:
        rented = "bike1"
    if status2[0] == 2:
        rented = "bike2"
    if status2[0] == 3:
        rented = "bike3"
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



def connection():
    connection = psycopg2.connect(user='postgres',
                                    password='11Chrzan',
                                    host='localhost',
                                    port='5432',
                                    database='mydb')
    connection.autocommit = True
    return connection


app = Flask(__name__)
app.config['SECRET_KEY'] = '123434211234342' # This has to be here for "form.validate_on_submit()" to work


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/user_register', methods=['GET', 'POST'])
def post_userdata():
    form = usersDataForm()
    # This try will take the data entered into the table on HTML and send it to the SQL server
    # If an except is not used an error will occur because it doesn't like the type of decimal field in WT-forms
    if form.is_submitted():
        try:
            con = connection()
            cursor = con.cursor()
            cursor.execute("INSERT INTO users VALUES('{}','{}');".format(form.usernameData.data, form.passwordData.data))
            con.commit()
            flash('Thanks for registering!', 'success')
        except IntegrityError:
            con = connection()
            con.rollback()
            flash('ERROR! Username ({}) already exists.'.format(form.usernameData.data), 'error')

    return render_template('user_register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def get_userdata():

    form = usersDataForm()
    if form.is_submitted():
        global username
        username = form.usernameData.data
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = '{}' AND pass = '{}';".format(form.usernameData.data, form.passwordData.data))
        status = cursor.fetchone()

        if status != None and username!="Admin":
            update_rented()
            return redirect('/user_profile')

        else:
            flash('username or/and password incorrect')

    return render_template('login.html', form=form)

################################################################################## Don't change anything above this line

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    update_rented()
    get_time()
    update_credits()
    return render_template('userprofile.html', username=username, rented=rented, credits=credits), rented

@app.route('/return', methods=['GET','POST'])
def returnbike():
    check_if_rented()
    if status[0]!=0:
        conn1=connection()
        cur1=conn1.cursor()
        sql1="UPDATE users SET rented=0 WHERE username='" + username + "';"
        sql2= "UPDATE bikes SET avaibility = 0 WHERE bike_name='" + rented + "';"
        sql3 = "SELECT rent_date FROM bikes WHERE bike_name='" + rented + "';"
        sql4 = "UPDATE bikes SET rent_date=NULL WHERE bike_name='" + rented + "';"
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
        return render_template("userprofile.html", username=username, rented=rented, credits=credits)
    if status[0] != 0:
        flash("You already have bike rented!")
        return render_template("userprofile.html", username=username, rented=rented, credits=credits), rented
    return render_template("rentbike.html"), rented

@app.route('/bike1', methods=['GET','POST'])
def rent_bike1():
    check_if_availble('bike1')
    if status_bike[0] == 0:
        get_time()
        conn1 = connection()
        cur1 = conn1.cursor()
        sql1 = "UPDATE users SET rented=1 WHERE username='" + username + "';"
        sql2 = "UPDATE bikes SET avaibility=1 WHERE bike_name='bike1';"
        #sql3 = "UPDATE bikes SET rent_date=" + datetime.datetime.now() + " WHERE bike_name='bike1'"
        sql3 = "UPDATE bikes SET rent_date=now() WHERE bike_name='bike1'"
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
    check_if_availble('bike2')
    if status_bike[0] == 0:
        conn1 = connection()
        cur1 = conn1.cursor()
        sql1 = "UPDATE users SET rented=2 WHERE username='" + username + "';"
        sql2 = "UPDATE bikes SET avaibility=1 WHERE bike_name='bike2';"
        sql3 = "UPDATE bikes SET rent_date=now() WHERE bike_name='bike2'"
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
    check_if_availble('bike3')
    if status_bike[0] == 0:
        conn1 = connection()
        cur1 = conn1.cursor()
        sql1 = "UPDATE users SET rented=3 WHERE username='" + username + "';"
        sql2 = "UPDATE bikes SET avaibility=1 WHERE bike_name='bike3';"
        sql3 = "UPDATE bikes SET rent_date=now() WHERE bike_name='bike3'"
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
    return render_template('rentbike.html', username=username, rented=rented),rented

@app.route('/credits', methods=['GET','POST'])
def add_credits():
    form = usersDataForm()
    if form.is_submitted():
        credits_to_add = form.creditsData.data
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT credits FROM users WHERE username='" + username + "';")
        credits_prev0 = cursor.fetchone()
        credits_prev=credits_prev0[0]
        credits_new= credits_to_add+credits_prev
        cursor.execute("UPDATE users SET credits={} WHERE username='{}'".format(credits_new, username))
        flash("Your credits were added!")
    return render_template('credits.html', form=form)


@app.route('/admin', methods=['GET','POST'])
def admin_login():
    form = usersDataForm()
    cur=connection().cursor()
    cur.execute("SELECT pass from users WHERE username='Admin'")
    password0= cur.fetchone()
    password= password0[0]
    if form.is_submitted():
        if form.usernameData.data == 'Admin' and form.passwordData.data == password:
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
    cursor.execute("SELECT * FROM bikes")
    bikes=cursor.fetchall()
    cursor.close()
    cursor=con.cursor()
    cursor.execute("SELECT * FROM users")
    users=cursor.fetchall()
    for row in bikes:
        a= {'bike_name': row[0], 'availblity': row[1], 'rent_date': row[2]}
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



################################################################################


if __name__ == '__main__':  # Allows to run the page by running the script in cmd

    app.run(debug=True)
