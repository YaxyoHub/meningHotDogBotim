import psycopg2
import os
from dotenv import load_dotenv
ORDERS_FILE = "orders.json"

load_dotenv()

def connect_psql():
    return psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT")
    )

def get_all_products():
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products ORDER BY id;")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_product_by_id(product_id):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products WHERE id = %s;", (product_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result if result else ("Noma’lum", 0)

def add_menu(name, price):
    conn = connect_psql()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM products WHERE name = %s;", (name,))
        if cursor.fetchone():
            return "❌ Bu nomdagi mahsulot allaqachon mavjud!"
        cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s);", (name, price))
        conn.commit()
        return "✅ Yangi mahsulot qo‘shildi!"
    except Exception as e:
        return f"Xatolik: {e}"
    finally:
        cursor.close()
        conn.close()

"""-----------------Admin------------------"""
def check_admin(tg_id):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id FROM admins WHERE tg_id = %s;", (tg_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data

def add_admin_sql(name, tg_id):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO admins (name, tg_id) VALUES (%s, %s);", (name, tg_id,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_admin_sql(tg_id):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admins WHERE tg_id = %s;", (tg_id,))
    conn.commit()
    cursor.close()
    conn.close()

"""-----------------Admin------------------"""
def delete_menu_sql(id):
    try:
        conn = connect_psql()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (id,))
        conn.commit()
        return "🗑 Menyu muvaffaqiyatli o‘chirildi!"
    except Exception as e:
        return f"❌ O‘chirishda xatolik: {e}"
    finally:
        cursor.close()
        conn.close()


def update_menu_sql(id, price):
    try:
        conn = connect_psql()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET price = %s WHERE id = %s", (price, id,))
        conn.commit()
    except Exception as e:
        print(f"❌ Yangilashda xatolik: {e}")
    finally:
        cursor.close()
        conn.close()