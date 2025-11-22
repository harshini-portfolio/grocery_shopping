from flask import Flask, request, render_template, redirect, session, url_for, jsonify
app = Flask(__name__)
app.secret_key = "abc"

conn = pymysql.connect(host="localhost", user="root", password="root", db="Grocery_shopping")
cursor = conn.cursor()
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/head")
def head():
    return render_template("head.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/admin_login_action", methods=['post'])
def admin_login_action():
    username = request.form.get("userName")
    password = request.form.get("password")
    print(username)
    print(password)
    if username == admin_username and password == admin_password:
        print("fff")
        session['role'] = 'admin'
        return redirect("/admin_home")
    else:
        return render_template("/message.html", message="Invalid Login Details")


@app.route("/admin_home")
def admin_home():
    return render_template("/admin_home.html")


@app.route("/user_login")
def user_login():
    return render_template("user_login.html")


@app.route("/user_login_action", methods=['post'])
def user_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from users where email='" + str(email) + "' and password='" + str(password) + "'")
    if count > 0:
        users = cursor.fetchall()
        session['user_id'] = users[0][0]
        session['role'] = 'user'
        return redirect("/user_home")
    else:
        return render_template("message.html", message="Invalid Login Details")


@app.route("/user_home")
def user_home():
    return render_template("user_home.html")

@app.route("/user_registration")
def user_registration():
    return render_template("user_registration.html")


@app.route("/user_registration_action", methods=['post'])
def user_registration_action():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from users where email='"+str(email)+"' ")
    if count > 0:
        return render_template("message.html", message="Duplicate Details Exist")
    else :
        cursor.execute("insert into users(username, email, password) values('"+str(username)+"','"+str(email)+"','"+str(password)+"')")
        conn.commit()
        return render_template("message.html", message="User Registered Successfully")

app.run(debug=True)
