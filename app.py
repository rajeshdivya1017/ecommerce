from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from db import get_connection
import os

app = Flask(__name__)

# =========================
# CONFIG
# =========================
app.secret_key = "ecommerce_secret_key"

app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

CORS(app, supports_credentials=True, resources={
    r"/api/*": {
        "origins": "http://localhost:5173",
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }
})

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response

bcrypt = Bcrypt(app)

# =========================
# IMAGE CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")

@app.route('/images/<filename>')
def serve_images(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

# =========================
# REGISTER
# =========================
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "customer")

    if not name or not email or not password:
        return jsonify({"message": "All fields required"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        return jsonify({"message": "Email exists"}), 400

    hashed = bcrypt.generate_password_hash(password).decode("utf-8")

    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, %s)
    """, (name, email, hashed, role))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Registered"}), 201

# =========================
# LOGIN
# =========================
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid login"}), 401

    session["user_id"] = user["id"]
    session["role"] = user["role"]
    session["name"] = user["name"]

    return jsonify({
        "message": "Login success",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    })

# =========================
# LOGOUT
# =========================
@app.route("/api/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

# =========================
# CURRENT USER
# =========================
@app.route("/api/me")
def me():
    if "user_id" not in session:
        return jsonify({"message": "Not logged in"}), 401

    return jsonify({
        "id": session["user_id"],
        "name": session["name"],
        "role": session["role"]
    })

# =========================
# PRODUCTS
# =========================
@app.route("/api/products")
def get_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.*, c.name AS category
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        ORDER BY p.id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)

# =========================
# SINGLE PRODUCT
# =========================
@app.route("/api/products/<int:id>")
def get_product(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.*, c.name AS category
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.id=%s
    """, (id,))

    product = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify(product)

# =========================
# ADMIN CHECK
# =========================
def is_admin():
    return session.get("role") == "admin"

# =========================
# ADD PRODUCT
# =========================
@app.route("/api/products", methods=["POST"])
def add_product():
    if not is_admin():
        return jsonify({"message": "Forbidden"}), 403

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (name, description, price, stock, category_id, image_url)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        data["name"],
        data.get("description"),
        data["price"],
        data["stock"],
        data["category_id"],
        data["image_url"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Product added"})

# =========================
# UPDATE PRODUCT
# =========================
@app.route("/api/products/<int:id>", methods=["PUT"])
def update_product(id):
    if not is_admin():
        return jsonify({"message": "Forbidden"}), 403

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET name=%s, description=%s, price=%s,
            stock=%s, category_id=%s, image_url=%s
        WHERE id=%s
    """, (
        data["name"],
        data.get("description"),
        data["price"],
        data["stock"],
        data["category_id"],
        data["image_url"],
        id
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Updated"})

# =========================
# DELETE PRODUCT
# =========================
@app.route("/api/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    if not is_admin():
        return jsonify({"message": "Forbidden"}), 403

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id=%s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Deleted"})

# =========================
# CREATE ORDER
# =========================
@app.route("/api/orders", methods=["POST", "OPTIONS"])
def create_order():
    if request.method == "OPTIONS":
        return '', 200

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"message": "Login required"}), 401

    data = request.json
    address = data.get("address")
    items = data.get("items", [])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    total = 0

    for i in items:
        cursor.execute("SELECT price FROM products WHERE id=%s", (i["product_id"],))
        p = cursor.fetchone()
        if p:
            total += p["price"] * i["quantity"]

    cursor.execute("""
        INSERT INTO orders (user_id, total_amount, status, address)
        VALUES (%s,%s,%s,%s)
    """, (user_id, total, "Pending", address))

    order_id = cursor.lastrowid

    for i in items:
        cursor.execute("SELECT price FROM products WHERE id=%s", (i["product_id"],))
        p = cursor.fetchone()
        if p:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                VALUES (%s,%s,%s,%s)
            """, (order_id, i["product_id"], i["quantity"], p["price"]))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Order placed"})

# =========================
# MY ORDERS (FIXED)
# =========================
@app.route("/api/orders/my")
def my_orders():
    if "user_id" not in session:
        return jsonify({"message": "Not logged in"}), 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM orders
        WHERE user_id=%s
        ORDER BY id DESC
    """, (session["user_id"],))

    orders = cursor.fetchall()

    for o in orders:
        cursor.execute("""
            SELECT oi.*, p.name AS product_name
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id=%s
        """, (o["id"],))

        o["items"] = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(orders)



@app.route("/api/admin/orders")
def admin_orders():

    if session.get("role") != "admin":
        return jsonify({"message": "Forbidden"}), 403

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT o.*,
               u.name AS customer_name
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.id DESC
    """)

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(orders)


# =========================
# UPDATE ORDER STATUS
# =========================
@app.route("/api/orders/<int:id>/status", methods=["PUT"])
def update_order_status(id):

    if session.get("role") != "admin":
        return jsonify({"message": "Forbidden"}), 403

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE orders SET status=%s WHERE id=%s",
        (data["status"], id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Order status updated successfully"})
# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)