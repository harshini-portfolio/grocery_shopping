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

@app.route("/add_stores")
def add_stores():
    cursor.execute("select * from stores")
    stores = cursor.fetchall()
    print(stores)
    return render_template("add_stores.html", stores=stores)

@app.route("/add_store", methods=['post'])
def add_store():
    cursor.execute("select * from stores")
    stores = cursor.fetchall()
    print(stores)
    return render_template("add_store.html", stores=stores)


@app.route("/add_store_action", methods=['post'])
def add_store_action():
    store_name = request.form.get("store_name")
    location = request.form.get("location")
    count = cursor.execute("select * from stores where store_name='" + str(store_name) + "'")
    if count > 0:
        return render_template("message.html", message="Duplicate Details Exist")
    cursor.execute("insert into stores(store_name,location) value('" + str(store_name)+ "','" + str(location)+ "')")
    conn.commit()
    return redirect("/add_stores")

@app.route("/edit_store")
def edit_store():
    store_id = request.args.get("store_id")
    cursor.execute("select * from stores where store_id=" + str(store_id))
    store = cursor.fetchone()
    return render_template("edit_store.html", store=store)

@app.route("/update_store", methods=['post'])
def update_store():
    store_id = request.form.get("store_id")
    store_name = request.form.get("store_name")
    location = request.form.get("location")

    cursor.execute("update stores set store_name='" + str(store_name) +
                   "', location='" + str(location) +
                   "' where store_id=" + str(store_id))
    conn.commit()
    return redirect("/add_stores")


@app.route("/delete_store")
def delete_store():
    store_id = request.args.get("store_id")
    cursor.execute("delete from stores where store_id=" + str(store_id))
    conn.commit()
    return redirect("/add_stores")

@app.route("/add_item")
def add_item():
    store_id = request.args.get("store_id")
    cursor.execute("select * from categories")
    categories = cursor.fetchall()
    cursor.execute("select * from items")
    items = cursor.fetchall()
    print(items)
    return render_template("/add_item.html",store_id=store_id,categories=categories,items=items,get_category_by_category_id=get_category_by_category_id)

@app.route("/add_items")
def add_items():
    store_id = request.args.get("store_id")
    cursor.execute("select * from categories")
    categories = cursor.fetchall()
    return render_template("/add_items.html",store_id=store_id,categories=categories)

@app.route("/add_items_action", methods=['post'])
def add_items_action():
    price = request.form.get("price")
    item_name = request.form.get("item_name")
    category_id = request.form.get("category_id")
    store_id = request.form.get("store_id")
    count = cursor.execute("select * from items where item_name='" + str(item_name) + "'")
    if count > 0:
        return render_template("message.html", message="Duplicate Details Exist")
    cursor.execute("insert into items(item_name,price,category_id,store_id) value('" + str(item_name) + "','" + str(price) + "','" + str(category_id) + "','" + str(store_id) + "')")
    conn.commit()
    return redirect("/add_item")

@app.route("/edit_item")
def edit_item():
    item_id = request.args.get("item_id")
    cursor.execute("select * from items where item_id=" + str(item_id))
    item = cursor.fetchone()

    cursor.execute("select * from categories")
    categories = cursor.fetchall()

    return render_template("edit_item.html", item=item, categories=categories)

@app.route("/update_item", methods=['post'])
def update_item():
    item_id = request.form.get("item_id")
    category_id = request.form.get("category_id")
    item_name = request.form.get("item_name")
    price = request.form.get("price")
    store_id = request.form.get("store_id")

    cursor.execute("update items set item_name='" + str(item_name) +
                   "', price='" + str(price) +
                   "', category_id='" + str(category_id) +
                   "' where item_id=" + str(item_id))
    conn.commit()

    return redirect("/add_item?store_id=" + str(store_id))

@app.route("/delete_item")
def delete_item():
    item_id = request.args.get("item_id")
    cursor.execute("delete from items where item_id=" + str(item_id))
    conn.commit()
    return redirect("/add_item")

@app.route("/add_to_cart",methods=['post'])
def add_to_cart():
    store_id = request.form.get("store_id")
    item_id= request.form.get("item_id")
    quantity = request.form.get("quantity")
    count = cursor.execute("select * from Shopping_lists where store_id='"+str(store_id)+"' and user_id='"+str(session['user_id'])+"' and status='Cart'")
    if count>0:
        Shopping_lists =cursor.fetchone()
        list_id = Shopping_lists[0]
    else:
        cursor.execute("insert into Shopping_lists(store_id,user_id,status,created_at) values ('"+str(store_id)+"','"+str(session['user_id'])+"','Cart','"+str(datetime.now())+"')")
        conn.commit()
        list_id = cursor.lastrowid
    count2 = cursor.execute("select * from list_items where list_id='"+str(list_id)+"' and item_id='"+str(item_id)+"'")
    if count2>0:
        existing_item = cursor.fetchone()
        new_quantity = int(existing_item[1]) + int(quantity)  # Assuming quantity is in column index 1
        cursor.execute(
            "update list_items set quantity='" + str(new_quantity) + "' where list_item_id='" + str(
                existing_item[0]) + "'"
        )
        conn.commit()
        return render_template("message1.html", message="Updated to cart")

    else:
        cursor.execute("insert into list_items(list_id,item_id,quantity,is_purchased) values ('"+str(list_id)+"','"+str(item_id)+"','"+str(quantity)+"','No')")
        conn.commit()
        return render_template("message1.html",message="Added to cart")

@app.route("/orders")
def orders():
    if session['role']=='admin':
        status = request.args.get("status", "cart").lower()  # default to cart if not provided

        status_map = {
            'cart': 'Cart',
            'ordered': 'Ordered',
            'dispatched': 'Dispatched',
            'history': 'Delivered'
        }

        db_status = status_map.get(status, 'Cart')  # fallback to Cart


        # Get shopping lists along with username
        cursor.execute("""
                    SELECT sl.list_id, sl.created_at, s.store_name, u.username,sl.status
                    FROM Shopping_lists sl
                    JOIN stores s ON sl.store_id = s.store_id
                    JOIN users u ON sl.user_id = u.user_id
                    WHERE  sl.status = %s
                """, (db_status))
        orders = cursor.fetchall()

        orders_data = []
        for order in orders:
            list_id, created_at, store_name, username, status = order

            # Get items for this shopping list
            cursor.execute("""
                        SELECT i.item_name, i.price, li.quantity, (i.price * li.quantity) as total_price, li.is_purchased,li.list_item_id
                        FROM list_items li
                        JOIN items i ON li.item_id = i.item_id
                        WHERE li.list_id = %s
                    """, (list_id,))
            items = cursor.fetchall()

            grand_total = sum(float(item[3]) for item in items)

            orders_data.append({
                'list_id': list_id,
                'created_at': created_at,
                'store_name': store_name,
                'username': username,  # now comes from DB
                'items': items,
                'grand_total': grand_total,
                "status": status
            })

        return render_template("orders.html", orders=orders_data, status=status)

    elif session['role']=='user':
        status = request.args.get("status", "cart").lower()  # default to cart if not provided

        status_map = {
            'cart': 'Cart',
            'ordered': 'Ordered',
            'dispatched': 'Dispatched',
            'history': 'Delivered'
        }

        db_status = status_map.get(status, 'Cart')  # fallback to Cart

        user_id = session['user_id']

        # Get shopping lists along with username
        cursor.execute("""
            SELECT sl.list_id, sl.created_at, s.store_name, u.username,sl.status
            FROM Shopping_lists sl
            JOIN stores s ON sl.store_id = s.store_id
            JOIN users u ON sl.user_id = u.user_id
            WHERE sl.user_id = %s AND sl.status = %s
        """, (user_id, db_status))
        orders = cursor.fetchall()

        orders_data = []
        for order in orders:
            list_id, created_at, store_name, username,status = order

            # Get items for this shopping list
            cursor.execute("""
                SELECT i.item_name, i.price, li.quantity, (i.price * li.quantity) as total_price, li.is_purchased,li.list_item_id
                FROM list_items li
                JOIN items i ON li.item_id = i.item_id
                WHERE li.list_id = %s
            """, (list_id,))
            items = cursor.fetchall()

            grand_total = sum(float(item[3]) for item in items)

            orders_data.append({
                'list_id': list_id,
                'created_at': created_at,
                'store_name': store_name,
                'username': username,  # now comes from DB
                'items': items,
                'grand_total': grand_total,
                "status":status
            })

        return render_template("orders.html", orders=orders_data, status=status)
@app.route("/remove")
def remove():
    list_id = request.args.get("list_id")
    list_item_id = request.args.get("list_item_id")
    cursor.execute("delete from list_items where list_item_id='"+str(list_item_id)+"'")
    conn.commit()
    count = cursor.execute("select * from list_items where list_id='"+str(list_id)+"'")
    if count==0:
        cursor.execute("delete from shopping_lists where list_id='" + str(list_id) + "'")
        conn.commit()
    return redirect("/orders")


@app.route("/place_order_now",methods=['post'])
def place_order_now():
    list_id = request.form.get("list_id")
    price = request.form.get("price")
    return render_template("place_order_now.html",price=price,list_id=list_id)

@app.route("/place_order_now_action",methods=['post'])
def place_order_now_action():
    list_id = request.form.get("list_id")
    print(list_id)
    cursor.execute("update list_items set is_purchased='Purchased' where list_id='" + str(list_id)+ "'")
    conn.commit()
    cursor.execute("update shopping_lists set status='Ordered' where list_id='" + str(list_id) + "'")
    conn.commit()
    return render_template("message1.html",message="Order Placed")

@app.route("/dispatch_order")
def dispatch_order():
    list_id = request.args.get("list_id")
    cursor.execute("update shopping_lists set status='Dispatched' where list_id='" + str(list_id) + "'")
    conn.commit()
    return render_template("message1.html",message="Order Dispatched")


@app.route("/mark_as_received")
def mark_as_received():
    list_id = request.args.get("list_id")
    cursor.execute("update shopping_lists set status='Delivered' where list_id='" + str(list_id) + "'")
    conn.commit()
    return render_template("message1.html",message="Order Delivered")

app.run(debug=True)
