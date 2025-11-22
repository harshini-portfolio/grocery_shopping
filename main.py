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


@app.route("/category_item_count")
def category_item_count():
    cursor.execute("""
        SELECT c.category_name, COUNT(i.item_id) 
        FROM categories c
        LEFT JOIN items i ON c.category_id = i.category_id
        GROUP BY c.category_id
    """)

    data = cursor.fetchall()

    result = {
        "labels": [row[0] for row in data],
        "counts": [row[1] for row in data]
    }

    return jsonify(result)

@app.route("/add_category")
def add_category():
    cursor.execute("select * from categories")
    categories = cursor.fetchall()
    return render_template("add_category.html", categories=categories)


@app.route("/add_category_action", methods=['POST'])
def add_category_action():
    category_name = request.form.get("category_name")
    count = cursor.execute("select * from categories where category_name='" + str(category_name) + "'")
    if count > 0:
        return redirect("/add_category")

    cursor.execute("insert into categories(category_name) value('" + str(category_name)+ "')")
    conn.commit()
    return redirect("/add_category")

@app.route("/edit_category")
def edit_category():
    category_id = request.args.get("category_id")
    cursor.execute("select*from categories where category_id='" + str(category_id) + "'")
    categories = cursor.fetchall()
    return render_template("edit_category.html",categories=categories[0],category_id=category_id)

@app.route("/edit_category_action")
def edit_category_action():
    category_id = request.args.get("category_id")
    category_name = request.args.get("category_name")
    cursor.execute("update categories set category_name='" + str(category_name) + "' where category_id='" + str(category_id) + "'")
    conn.commit()
    return redirect("/add_category")


@app.route("/delete_category")
def delete_category():
    category_id = request.args.get("category_id")
    cursor.execute("delete from categories where category_id='" + str(category_id) + "'")
    conn.commit()
    return redirect("/add_category")

app.run(debug=True)
