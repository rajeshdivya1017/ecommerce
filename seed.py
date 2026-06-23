import mysql.connector
from flask_bcrypt import Bcrypt

# =========================
# DB CONNECTION
# =========================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="$Divya@1010",   # change if needed
    database="ecommerce"
)

cursor = db.cursor()
bcrypt = Bcrypt()

# =========================
# RESET DATABASE (SAFE ORDER)
# =========================
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

cursor.execute("DELETE FROM order_items")
cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM products")
cursor.execute("DELETE FROM categories")
cursor.execute("DELETE FROM users")

cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# =========================
# USERS
# =========================
admin_pass = bcrypt.generate_password_hash("admin123").decode('utf-8')
user_pass = bcrypt.generate_password_hash("user123").decode('utf-8')

cursor.execute("""
INSERT INTO users (name, email, password, role)
VALUES (%s, %s, %s, %s)
""", ("Admin", "admin@shop.com", admin_pass, "admin"))

cursor.execute("""
INSERT INTO users (name, email, password, role)
VALUES (%s, %s, %s, %s)
""", ("User", "user@shop.com", user_pass, "customer"))

# =========================
# CATEGORIES
# =========================
categories = [
    ("Electronics",),
    ("Groceries",),
    ("Toys",),
    ("Beauty",),
    ("Fashion",),
    ("Books",),
    ("Home & Kitchen",),
    ("Sports",)
]

cursor.executemany(
    "INSERT INTO categories (name) VALUES (%s)",
    categories
)

db.commit()

# category map
cursor.execute("SELECT id, name FROM categories")
cat_map = {name: id for (id, name) in cursor.fetchall()}

# =========================
# PRODUCTS (FIXED IMAGES)
# =========================
products = [
    ("Laptop", "High performance laptop", 55000, 10, "Electronics",
     "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&q=80"),

    ("Smartphone", "Latest Android phone", 25000, 20, "Electronics",
     "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80"),

    ("Headphones", "Noise cancelling headphones", 3000, 30, "Electronics",
     "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80"),

    ("Smart Watch", "Fitness tracker watch", 4000, 25, "Electronics",
     "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80"),

    ("Bluetooth Speaker", "Portable speaker", 1500, 35, "Electronics",
     "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?auto=format&fit=crop&w=600&q=80"),

    # ---------------- GROCERIES (FIXED IMAGES) ----------------
("Rice Bag", "Premium quality rice 5kg", 450, 50, "Groceries",
 "https://images.unsplash.com/photo-1603048297172-c92544798d5a?auto=format&fit=crop&w=600&q=80"),

("Wheat Flour", "Fresh wheat flour 5kg pack", 300, 40, "Groceries",
 "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=600&q=80"),

("Cooking Oil", "Refined sunflower oil 1L", 180, 60, "Groceries",
 "https://images.unsplash.com/photo-1620706857370-e1b9770e8bb1?auto=format&fit=crop&w=600&q=80"),

("Sugar", "White refined sugar 1kg", 60, 80, "Groceries",
 "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&w=600&q=80"),

    ("Toy Car", "Remote car", 800, 30, "Toys",
     "https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?auto=format&fit=crop&w=600&q=80"),

    ("Lego Set", "Building blocks", 1200, 25, "Toys",
     "https://images.unsplash.com/photo-1587654780291-39c9404d746b?auto=format&fit=crop&w=600&q=80"),

    ("Doll", "Kids doll", 500, 40, "Toys",
     "https://images.unsplash.com/photo-1519689680058-324335c77eba?auto=format&fit=crop&w=600&q=80"),

    ("Lipstick", "Matte lipstick", 250, 60, "Beauty",
     "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=600&q=80"),

    ("Face Cream", "Skin care cream", 350, 45, "Beauty",
     "https://images.unsplash.com/photo-1556228578-8c89e6adf883?auto=format&fit=crop&w=600&q=80"),

    ("Perfume", "Luxury perfume", 1200, 30, "Beauty",
     "https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=600&q=80"),

    ("T-Shirt", "Cotton shirt", 500, 50, "Fashion",
     "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=600&q=80"),

    ("Jeans", "Slim fit jeans", 1200, 40, "Fashion",
     "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=600&q=80"),

    ("Shoes", "Running shoes", 2000, 35, "Fashion",
     "https://images.unsplash.com/photo-1528701800489-20be3c4ea4f2?auto=format&fit=crop&w=600&q=80"),

    ("Python Book", "Learn Python", 500, 30, "Books",
     "https://images.unsplash.com/photo-1512820790803-83ca734da9c0?auto=format&fit=crop&w=600&q=80"),

    ("AI Basics", "AI introduction", 600, 20, "Books",
     "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=600&q=80"),

    ("Mixer Grinder", "Kitchen appliance", 2500, 20, "Home & Kitchen",
     "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=600&q=80"),

    ("Kettle", "Electric kettle", 900, 30, "Home & Kitchen",
     "https://images.unsplash.com/photo-1594223274512-ad4803739b7c?auto=format&fit=crop&w=600&q=80"),

    ("Water Bottle", "Steel bottle", 300, 50, "Home & Kitchen",
     "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=600&q=80"),

    ("Football", "Sports ball", 800, 40, "Sports",
     "https://images.unsplash.com/photo-1575361204480-aadea25e6e68?auto=format&fit=crop&w=600&q=80"),

    ("Cricket Bat", "Pro bat", 1500, 25, "Sports",
     "https://images.unsplash.com/photo-1593766788306-28561a7e95b0?auto=format&fit=crop&w=600&q=80"),

    ("Basketball", "Indoor ball", 900, 30, "Sports",
     "https://images.unsplash.com/photo-1519861531473-9200262188bf?auto=format&fit=crop&w=600&q=80"),
]

# =========================
# INSERT PRODUCTS
# =========================
for name, desc, price, stock, cat, img in products:
    cursor.execute("""
        INSERT INTO products (name, description, price, stock, category_id, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, desc, price, stock, cat_map[cat], img))

db.commit()

cursor.close()
db.close()

print("✅ Seed completed successfully (NO ERRORS + IMAGES FIXED)")