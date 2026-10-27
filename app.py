import os
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret")
DB_CONFIG = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432"),
    "dbname": os.getenv("PGDATABASE", "shreya_pise_om_sales"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", "")
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/")
def dashboard():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT COUNT(*) AS n FROM products"); products_count = cur.fetchone()["n"]
            cur.execute("SELECT COUNT(*) AS n FROM retailers"); retailers_count = cur.fetchone()["n"]
            cur.execute("SELECT COUNT(*) AS n FROM sales_orders"); orders_count = cur.fetchone()["n"]
            cur.execute("SELECT COALESCE(SUM(total_amount),0) AS total FROM sales_orders WHERE order_status <> 'Cancelled'")
            revenue = cur.fetchone()["total"]
            cur.execute("""SELECT so.order_id, r.retailer_name, so.order_date, so.order_status, so.total_amount
                           FROM sales_orders so JOIN retailers r ON r.retailer_id=so.retailer_id
                           ORDER BY so.order_id DESC LIMIT 8""")
            recent_orders = cur.fetchall()
            cur.execute("""SELECT p.product_name, p.category, p.stock_quantity, p.selling_price, s.supplier_name
                           FROM products p JOIN suppliers s ON s.supplier_id=p.supplier_id
                           ORDER BY p.product_id LIMIT 8""")
            product_rows = cur.fetchall()
    finally:
        conn.close()
    return render_template("index.html", products_count=products_count, retailers_count=retailers_count,
                           orders_count=orders_count, revenue=revenue, recent_orders=recent_orders,
                           product_rows=product_rows)

@app.route("/products", methods=["GET", "POST"])
def products():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if request.method == "POST":
                name = request.form["product_name"].strip()
                category = request.form["category"]
                price = request.form["selling_price"]
                stock = request.form["stock_quantity"]
                supplier_id = request.form["supplier_id"]
                cur.execute("""INSERT INTO products(product_name, category, selling_price, stock_quantity, supplier_id)
                               VALUES (%s,%s,%s,%s,%s)""", (name, category, price, stock, supplier_id))
                conn.commit()
                flash("Product added successfully.", "success")
                return redirect(url_for("products"))
            cur.execute("SELECT supplier_id, supplier_name FROM suppliers ORDER BY supplier_name")
            supplier_rows = cur.fetchall()
            cur.execute("""SELECT p.product_id,p.product_name,p.category,p.selling_price,p.stock_quantity,s.supplier_name
                           FROM products p JOIN suppliers s ON s.supplier_id=p.supplier_id ORDER BY p.product_id""")
            rows = cur.fetchall()
    finally:
        conn.close()
    return render_template("products.html", rows=rows, supplier_rows=supplier_rows)

@app.route("/retailers")
def retailer_page():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM retailers ORDER BY retailer_id")
            rows = cur.fetchall()
    finally:
        conn.close()
    return render_template("retailers.html", rows=rows)

@app.route("/orders")
def orders():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""SELECT so.order_id,r.retailer_name,so.order_date,so.order_status,so.total_amount
                           FROM sales_orders so JOIN retailers r ON r.retailer_id=so.retailer_id
                           ORDER BY so.order_id DESC""")
            rows = cur.fetchall()
    finally:
        conn.close()
    return render_template("orders.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
