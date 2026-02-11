from flask import Flask, render_template, request, redirect, session,jsonify, flash, url_for,current_app
from werkzeug.security import generate_password_hash, check_password_hash
from io import BytesIO
from flask import send_file
from datetime import datetime
from collections import defaultdict
import mysql.connector
import qrcode
import os
import time
import requests
import re
import random
import math


app = Flask(__name__)


# ================= SECRET KEY =================
app.secret_key = os.getenv("SECRET_KEY", "logistik-barang")

# ================= KONEKSI DATABASE =================
def get_db_connection_azka():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
def normalize_address(address):
    address = address.lower()
    address = address.replace("no.", "")
    address = address.replace("jl.", "jalan")
    address = address.replace("kec.", "")
    address = address.replace("kab.", "")
    address = address.replace("kota", "")
    return address.strip()

def get_lat_lng_city_from_address(address):
    try:
        time.sleep(1)
        clean_address = normalize_address(address)

        url = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "LogisticsAzka/1.0"}

        res = requests.get(
            url,
            params={
                "q": clean_address,
                "format": "json",
                "limit": 1,
                "addressdetails": 1
            },
            headers=headers,
            timeout=10
        )

        data = res.json()

        if data:
            lat = float(data[0]["lat"])
            lng = float(data[0]["lon"])
            addr = data[0].get("address", {})

            city = (
                addr.get("city")
                or addr.get("town")
                or addr.get("county")
                or addr.get("state")
                or "TIDAK DIKETAHUI"
            )

            return lat, lng, city.upper()

    except Exception as e:
        print("Geocoding error:", e)

    return None, None, "TIDAK DIKETAHUI"


def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name.lower())
def get_description(status, warehouse_name, is_interisland):
    if status == 'PICKUP':
        return "📦 Paket telah diserahkan kepada driver"

    # SETELAH PICKUP + SCAN OUT
    if status == 'ARRIVED_AT_ORIGIN_HUB':
        return f"🚚 Paket telah keluar dari gudang asal {warehouse_name}"

    if status == 'IN_TRANSIT':
        if is_interisland:
            return f"🚢 Paket sedang dalam pengiriman antar pulau dari {warehouse_name}"
        return f"🚛 Paket sedang dalam perjalanan dari {warehouse_name}"

    if status == 'SORTING':
        return f"📦 Paket sedang disortir di hub {warehouse_name}"

    if status == 'READY_FOR_DELIVERY':
        return "📍 Paket siap dikirim ke alamat penerima"

    return "-"

def haversine(lat1, lon1, lat2, lon2):
    # PAKSA SEMUA KE FLOAT
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    R = 6371  # KM

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
@app.route('/', methods=['GET', 'POST'])
@app.route('/login_azka', methods=['GET', 'POST'])
def login_azka():
    if request.method == "POST":
        username_azka = request.form['username_azka']
        password_azka = request.form['password_azka']

        conn = get_db_connection_azka()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_azka,
                username_azka,
                password_hash_azka,
                role_id_azka,
                warehouse_id_azka
            FROM tbl_users_azka
            WHERE username_azka=%s
        """, (username_azka,))

        user_azka = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user_azka:
            flash("Username tidak ditemukan!", "danger")
            return redirect(url_for('login_azka'))

        if not check_password_hash(
            user_azka['password_hash_azka'],
            password_azka
        ):
            flash("Password salah!", "danger")
            return redirect(url_for('login_azka'))

        # 🔐 RESET SESSION
        session.clear()

        # ✅ SESSION WAJIB
        session['user_id_azka'] = user_azka['id_azka']
        session['username_azka'] = user_azka['username_azka']
        session['role_id_azka'] = user_azka['role_id_azka']

        # 🔥 INI KUNCI UTAMA
        session['warehouse_id_azka'] = user_azka['warehouse_id_azka']

        insert_log_azka(
            user_azka['id_azka'],
            "Login",
            f"User {user_azka['username_azka']} berhasil login"
        )

        flash("Login berhasil!", "success")
        return redirect(url_for('dashboard_azka'))

    return render_template("login_azka.html")

@app.route('/generate_qr/<tracking_number>')
def generate_qr(tracking_number):
    # Generate QR code for the tracking number
    qr = qrcode.make(tracking_number)
    img = BytesIO()
    qr.save(img, 'PNG')
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/dashboard_azka')
def dashboard_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login terlebih dahulu!", "warning")
        return redirect(url_for('login_azka'))

    role_azka = session.get('role_id_azka')
    
    dashboard_map_azka = {
        1: 'admin_dashboard_azka',
        2: 'gudang_dashboard_azka',
        3: 'kurir_dashboard_azka',
        4: 'manager_dashboard_azka',
        5: 'dashboard_sopir_azka'
    }

    if role_azka in dashboard_map_azka:
        return redirect(url_for(dashboard_map_azka[role_azka]))

    flash("Role tidak dikenali!", "danger")
    return redirect(url_for('login_azka'))

# ===========================
#   ADMIN DASHBOARD
# ===========================
@app.route('/admin_dashboard_azka')
def admin_dashboard_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') != 1:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    #tahun_azka = request.args.get('tahun_azka')

    conn_azka = get_db_connection_azka()
    cursor_azka = conn_azka.cursor(dictionary=True)


    tables_azka = {
        "total_users_azka": "tbl_users_azka",
        "total_warehouses_azka": "tbl_warehouses_azka",
        "total_shipment_azka": "tbl_shipment_azka",
        "total_logs_azka": "tbl_activity_logs_azka"
    }

    totals_azka = {}
    for key_azka, table_azka in tables_azka.items():
        cursor_azka.execute(f"SELECT COUNT(*) AS total_azka FROM {table_azka}")
        totals_azka[key_azka] = cursor_azka.fetchone()['total_azka']

    # ===================== TOTAL KURIR =====================
    cursor_azka.execute("""
        SELECT COUNT(*) AS total_couriers_azka
        FROM tbl_users_azka
        WHERE role_id_azka = 3
    """)
    total_couriers_azka = cursor_azka.fetchone()['total_couriers_azka']

    cursor_azka.execute("""
        SELECT COUNT(*) AS courier_online_azka
        FROM tbl_users_azka
        WHERE role_id_azka = 3
        AND last_activity IS NOT NULL
    """)
    courier_online_azka = cursor_azka.fetchone()['courier_online_azka']


    cursor_azka.execute("""
        SELECT COUNT(*) AS courier_offline_azka
        FROM tbl_users_azka
        WHERE role_id_azka = 3
        AND last_activity IS NULL
    """)
    courier_offline_azka = cursor_azka.fetchone()['courier_offline_azka']

        # ===================== STATUS SHIPMENT =====================
    status_list_azka = [
        'CREATED',
        'PICKUP',
        'ARRIVED_AT_ORIGIN_HUB',
        'IN_TRANSIT',
        'SORTING',
        'READY_FOR_DELIVERY',
        'DELIVERED'
    ]


    status_count_azka = {}
    for status_azka in status_list_azka:
        cursor_azka.execute("""
            SELECT COUNT(*) AS total_azka
            FROM tbl_shipment_azka
            WHERE status_azka = %s
        """, (status_azka,))
        status_count_azka[status_azka] = cursor_azka.fetchone()['total_azka']

        # ===================== LOG PAKET PER SHIPMENT =====================
    cursor_azka.execute("""
        SELECT
        s.id_azka AS shipment_id_azka,
        s.tracking_number_azka,
        s.status_azka,

        u.username_azka AS nama_aktor_azka,
        CASE
            WHEN u.role_id_azka = 3 THEN 'KURIR'
            WHEN u.role_id_azka = 5 THEN 'Driver'
            ELSE 'Gudang'
        END AS role_aktor_azka,

        l.actions_azka AS deskripsi_azka,
        l.created_at_azka
    FROM tbl_activity_logs_azka l
    JOIN tbl_users_azka u ON l.user_id_azka = u.id_azka
    JOIN tbl_shipment_azka s
        ON l.actions_azka LIKE CONCAT('%', s.tracking_number_azka, '%')
    WHERE l.actions_azka LIKE '%Paket%'
    ORDER BY s.id_azka, l.created_at_azka DESC;
    """)

    raw_logs_azka = cursor_azka.fetchall()
    shipment_logs_azka = {}

    for row in raw_logs_azka:
        sid = row['shipment_id_azka']

        if sid not in shipment_logs_azka:
            shipment_logs_azka[sid] = {
                "shipment_id_azka": sid,
                "tracking_number_azka": row['tracking_number_azka'],
                "status_azka": row['status_azka'],
                "logs": []
            }

        shipment_logs_azka[sid]["logs"].append({
            "nama_aktor_azka": row['nama_aktor_azka'],
            "role_aktor_azka": row['role_aktor_azka'],
            "deskripsi_azka": row['deskripsi_azka'],
            "created_at_azka": row['created_at_azka']
        })

    shipment_logs_azka = list(shipment_logs_azka.values())


    # ===================== POSISI KURIR TERKINI =====================
    cursor_azka.execute("""
        SELECT 
            u.id_azka,
            u.username_azka,
            u.role_id_azka,
            CASE 
                WHEN u.role_id_azka = 5 THEN 'DRIVER'
                WHEN u.role_id_azka = 3 THEN 'KURIR'
            END AS user_type,
            w.nama_azka AS warehouse_name_azka,
            w.address_azka,
            s.scan_type_azka,
            s.scan_time_azka
        FROM tbl_users_azka u
        LEFT JOIN (
            -- ===== DRIVER SCAN TERAKHIR =====
            SELECT 
                ds.driver_id_azka AS user_id,
                ds.warehouse_id_azka,
                ds.scan_type_azka,
                ds.scan_time_azka
            FROM tbl_driver_scans_azka ds
            JOIN (
                SELECT driver_id_azka, MAX(scan_time_azka) last_scan
                FROM tbl_driver_scans_azka
                GROUP BY driver_id_azka
            ) x ON ds.driver_id_azka = x.driver_id_azka
            AND ds.scan_time_azka = x.last_scan

            UNION ALL

            -- ===== KURIR SCAN TERAKHIR =====
            SELECT 
                cs.courier_id_azka AS user_id,
                cs.warehouse_id_azka,
                cs.scan_type_azka,
                cs.scan_time_azka
            FROM tbl_courier_scans_azka cs
            JOIN (
                SELECT courier_id_azka, MAX(scan_time_azka) last_scan
                FROM tbl_courier_scans_azka
                GROUP BY courier_id_azka
            ) y ON cs.courier_id_azka = y.courier_id_azka
            AND cs.scan_time_azka = y.last_scan
        ) s ON u.id_azka = s.user_id
        LEFT JOIN tbl_warehouses_azka w
            ON s.warehouse_id_azka = w.id_azka
        WHERE u.role_id_azka IN (3,5)
        ORDER BY u.username_azka;
    """)

    courier_position_azka = cursor_azka.fetchall()

    # ===================== LOG SCAN KURIR (MONITORING) =====================
    cursor_azka.execute("""
        SELECT 
            u.username_azka,
            cs.scan_type_azka,
            w.nama_azka AS warehouse_name_azka,
            cs.scan_time_azka
        FROM tbl_courier_scans_azka cs
        JOIN tbl_users_azka u ON cs.courier_id_azka = u.id_azka
        LEFT JOIN tbl_warehouses_azka w ON cs.warehouse_id_azka = w.id_azka
        LEFT JOIN tbl_driver_scans_azka b ON b.driver_id_azka = u.id_azka
        ORDER BY cs.scan_time_azka DESC
        LIMIT 10
    """)
    courier_scan_logs_azka = cursor_azka.fetchall()
    # ===================== KURIR DI DALAM GUDANG =====================
    cursor_azka.execute("""
        SELECT COUNT(DISTINCT cs.courier_id_azka) AS total
        FROM tbl_courier_scans_azka cs
        JOIN (
            SELECT courier_id_azka, MAX(scan_time_azka) AS last_scan
            FROM tbl_courier_scans_azka
            GROUP BY courier_id_azka
        ) last_scan
        ON cs.courier_id_azka = last_scan.courier_id_azka
        AND cs.scan_time_azka = last_scan.last_scan
        WHERE cs.scan_type_azka = 'IN'
    """)
    courier_inside_azka = cursor_azka.fetchone()['total']

    # ===================== KURIR DI LUAR =====================
    cursor_azka.execute("""
        SELECT COUNT(DISTINCT cs.courier_id_azka) AS total
        FROM tbl_courier_scans_azka cs
        JOIN (
            SELECT courier_id_azka, MAX(scan_time_azka) AS last_scan
            FROM tbl_courier_scans_azka
            GROUP BY courier_id_azka
        ) last_scan
        ON cs.courier_id_azka = last_scan.courier_id_azka
        AND cs.scan_time_azka = last_scan.last_scan
        WHERE cs.scan_type_azka = 'OUT'
    """)
    courier_outside_azka = cursor_azka.fetchone()['total']

    conn_azka.close()

    return render_template(
    "admin_dashboard_azka.html",
    username_azka=session['username_azka'],

    #tahun_azka=tahun_azka,
    #list_tahun_azka=list_tahun_azka,

    **totals_azka,
    shipment_logs_azka=shipment_logs_azka,

    total_couriers_azka=total_couriers_azka,
    courier_inside_azka=courier_inside_azka,
    courier_outside_azka=courier_outside_azka,

    courier_scan_logs_azka=courier_scan_logs_azka,
    courier_position_azka=courier_position_azka,

    #barang_masuk_azka=map_bulan_azka(barang_masuk_raw_azka),
    #barang_keluar_azka=map_bulan_azka(barang_keluar_raw_azka),
)


@app.before_request
def update_last_activity():
    if 'user_id_azka' in session:
        conn = get_db_connection_azka()
        cursor = conn.cursor()
        cursor.execute("UPDATE tbl_users_azka SET last_activity = NOW() WHERE id_azka = %s", (session['user_id_azka'],))
        conn.commit()
        cursor.close()
        conn.close()

@app.route('/admin_users_azka')
def admin_users_azka():
    if 'user_id_azka' not in session or session.get('role_id_azka') != 1:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('login_azka'))



    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # Ambil semua user
    cursor.execute("""
        SELECT u.id_azka, u.username_azka, u.email_azka,
            r.nama_azka, u.created_at_azka, u.is_active_azka,
            CASE 
                WHEN u.last_activity >= NOW() - INTERVAL 5 MINUTE THEN 1
                ELSE 0
            END AS status_online
        FROM tbl_users_azka u
        JOIN tbl_roles_azka r ON u.role_id_azka = r.id_azka
        ORDER BY u.created_at_azka DESC
    """)

    users = cursor.fetchall()

    cursor.execute("""
        SELECT id_azka, nama_azka 
        FROM tbl_roles_azka
    """)
    roles_azka = cursor.fetchall()

    

    cursor.close()
    conn.close()

    return render_template(
        'admin_users_azka.html',
        users=users,
        roles_azka=roles_azka,
        username_azka=session.get('username_azka')
    )

@app.route('/admin_users_add_azka', methods=['GET', 'POST'])
def admin_users_add_azka():
    if 'user_id_azka' not in session or session.get('role_id_azka') != 1:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('login_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)



    if request.method == 'POST':
        username_azka = request.form['username_azka']
        email_azka = request.form['email_azka']
        password_hash_azka = request.form['password_hash_azka']
        role_id_azka = request.form['role_id_azka']

        password_hash_azka = generate_password_hash(
            password_hash_azka,
            method='pbkdf2:sha256',
            salt_length=16
        )

        cursor.execute("""
            INSERT INTO tbl_users_azka
            (username_azka, email_azka, password_hash_azka, role_id_azka, is_active_azka)
            VALUES (%s, %s, %s, %s, 1)
        """, (
            username_azka,
            email_azka,
            password_hash_azka,
            role_id_azka
        ))

        conn.commit()
        flash("User berhasil ditambahkan!", "success")

        cursor.close()
        conn.close()
        return redirect(url_for('admin_users_azka'))

    cursor.close()
    conn.close()

    return render_template(
        'admin_users_azka.html',
        roles_azka=roles_azka,
        username_azka=session.get('username_azka')
    )

@app.route('/admin_users_edit_azka/<int:id_azka>', methods=['POST'])
def admin_users_edit_azka(id_azka):
    if 'user_id_azka' not in session or session.get('role_id_azka') != 1:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('login_azka'))

    username_azka = request.form['username_azka']
    email_azka = request.form['email_azka']
    role_id_azka = request.form['role_id_azka']
    is_active_azka = request.form['is_active_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_users_azka
        SET username_azka=%s,
            email_azka=%s,
            role_id_azka=%s,
            is_active_azka=%s
        WHERE id_azka=%s
    """, (
        username_azka,
        email_azka,
        role_id_azka,
        is_active_azka,
        id_azka
    ))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Data user berhasil diperbarui!", "success")
    return redirect(url_for('admin_users_azka'))
@app.route('/admin_users_reset_password_azka/<int:id_azka>', methods=['POST'])
def admin_users_reset_password_azka(id_azka):
    if 'user_id_azka' not in session or session.get('role_id_azka') != 1:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('login_azka'))

    password_hash_azka = request.form['password_hash_azka']
    password_confirm_azka = request.form['password_confirm_azka']

    if password_hash_azka != password_confirm_azka:
        flash("Password tidak cocok!", "danger")
        return redirect(url_for('admin_users_azka'))

    password_hash_azka = generate_password_hash(
        password_hash_azka,
        method='pbkdf2:sha256',
        salt_length=16
    )

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_users_azka
        SET password_hash_azka=%s
        WHERE id_azka=%s
    """, (password_hash_azka, id_azka))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Password berhasil di-reset!", "success")
    return redirect(url_for('admin_users_azka'))
@app.route('/admin_users_delete_azka/<int:id_azka>', methods=['POST'])
def admin_users_delete_azka(id_azka):

    if 'user_id_azka' not in session or session.get('role_id_azka') != 1:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('login_azka'))

    if session.get('user_id_azka') == id_azka:
        flash("Anda tidak dapat menghapus akun sendiri!", "warning")
        return redirect(url_for('admin_users_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tbl_users_azka WHERE id_azka = %s",
        (id_azka,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("User berhasil dihapus!", "success")
    return redirect(url_for('admin_users_azka'))

# ===========================
#   ACTIVITY LOGS PAGE
# ===========================
def insert_log_azka(user_id, action, description):
    try:
        conn = get_db_connection_azka()
        cursor = conn.cursor()

        query = """
            INSERT INTO tbl_activity_logs_azka 
            (user_id_azka, actions_azka, reference_azka)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (user_id, action, description))
        conn.commit()
    except Exception as e:
        print("ERROR INSERT LOG:", e)
    finally:
        cursor.close()
        conn.close()


@app.route('/activity_logs_azka')
def activity_logs_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') != 1:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    sys_page = request.args.get('sys_page', default=1, type=int)
    act_page = request.args.get('act_page', default=1, type=int)

    limit = 15
    sys_offset = (sys_page - 1) * limit
    act_offset = (act_page - 1) * limit

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # ============ SYSTEM LOGS ============  
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tbl_activity_logs_azka
        WHERE actions_azka IN ('Login','Logout')
    """)
    sys_total = cursor.fetchone()['total']
    sys_pages = (sys_total + limit - 1) // limit

    cursor.execute("""
        SELECT l.*, u.username_azka, r.nama_azka
        FROM tbl_activity_logs_azka l
        INNER JOIN tbl_users_azka u ON l.user_id_azka = u.id_azka
        INNER JOIN tbl_roles_azka r ON u.role_id_azka = r.id_azka
        WHERE l.actions_azka IN ('Login','Logout')
        ORDER BY l.created_at_azka DESC
        LIMIT %s OFFSET %s
    """, (limit, sys_offset))
    system_logs = cursor.fetchall()

    # ============ ACTIVITY LOGS ============  
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tbl_activity_logs_azka
        WHERE actions_azka NOT IN ('Login','Logout')
    """)
    act_total = cursor.fetchone()['total']
    act_pages = (act_total + limit - 1) // limit

    cursor.execute("""
        SELECT l.*, u.username_azka, r.nama_azka
        FROM tbl_activity_logs_azka l
        INNER JOIN tbl_users_azka u ON l.user_id_azka = u.id_azka
        INNER JOIN tbl_roles_azka r ON u.role_id_azka = r.id_azka
        WHERE l.actions_azka NOT IN ('Login','Logout')
        ORDER BY l.created_at_azka DESC
        LIMIT %s OFFSET %s
    """, (limit, act_offset))
    activity_logs = cursor.fetchall()

    conn.close()

    return render_template(
        "activity_logs_azka.html",
        username_azka=session['username_azka'],
        system_logs=system_logs,
        activity_logs=activity_logs,
        sys_page=sys_page,
        sys_pages=sys_pages,
        act_page=act_page,
        act_pages=act_pages
    )

# ===========================
#   DATA BARANG 
# ===========================
@app.route('/product_azka')
def product_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in (1, 2):
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            l.id_azka,
            l.sku_azka,
            l.nama_product_azka,
            u.nama_azka AS category_name,
            l.category_id_azka,
            l.unit_azka,
            l.min_stock_azka
        FROM tbl_products_azka l
        INNER JOIN tbl_product_categories_azka u 
            ON l.category_id_azka = u.id_azka
            
        
    """)
    product_azka = cursor.fetchall()

    cursor.execute('SELECT id_azka, nama_azka FROM tbl_product_categories_azka ORDER BY id_azka ASC')
    categories = cursor.fetchall()

    conn.close()

    return render_template(
        "product_azka.html",
                username_azka=session['username_azka'],
        product_azka=product_azka,
        categories=categories
    )

@app.route('/product_edit_azka/<int:id_azka>', methods=['GET', 'POST'])
def product_edit_azka(id_azka):
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        sku = request.form['sku_azka']
        nama = request.form['nama_azka']
        category = request.form['category_id_azka']
        unit = request.form['unit_azka']
        min_stock = request.form['min_stock_azka']

        cursor.execute("""
            UPDATE tbl_products_azka SET
                sku_azka=%s,
                nama_product_azka=%s,
                category_id_azka=%s,
                unit_azka=%s,
                min_stock_azka=%s
            WHERE id_azka=%s
        """, (sku, nama, category, unit, min_stock, id_azka))
        conn.commit()

        cursor.close()
        conn.close()

        insert_log_azka(session['user_id_azka'], "Edit", f"Edit barang: {nama}")
        flash("Barang berhasil diperbarui!", "success")
        return redirect(url_for('product_azka'))

    cursor.execute("SELECT * FROM tbl_products_azka WHERE id_azka=%s", (id_azka,))
    product = cursor.fetchone()

    cursor.execute("SELECT * FROM tbl_product_categories_azka")
    categories = cursor.fetchall()

    conn.close()

    return render_template(
        "product_azka.html",
        product=product,
        categories=categories,
        username_azka=session['username_azka']
    )

@app.route('/product_delete_azka/<int:id_azka>', methods=['GET'])
def product_delete_azka(id_azka):
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("SELECT nama_azka FROM tbl_products_azka WHERE id_azka=%s", (id_azka,))
    row = cursor.fetchone()
    nama_barang = row[0] if row else "Tidak diketahui"

    cursor.execute("DELETE FROM tbl_products_azka WHERE id_azka=%s", (id_azka,))
    conn.commit()

    conn.close()

    insert_log_azka(session['user_id_azka'], "Delete", f"Hapus barang: {nama_barang}")

    flash("Barang berhasil dihapus!", "danger")
    return redirect(url_for('product_azka'))

@app.route('/gudang_azka')
def gudang_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') != 1:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            id_azka,
            nama_azka,
            address_azka
        FROM tbl_warehouses_azka
    """)
    gudang_azka = cursor.fetchall()

    conn.close()

    return render_template(
        "gudang_azka.html",
        username_azka=session['username_azka'],
        gudang_azka=gudang_azka
    )
@app.route('/qr_gudang_azka/<int:warehouse_id>')
def qr_gudang_azka(warehouse_id):
    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_azka, nama_azka, qr_code_data_azka
        FROM tbl_warehouses_azka
        WHERE id_azka = %s
    """, (warehouse_id,))
    gudang_azka = cursor.fetchone()
    conn.close()

    if not gudang_azka:
        return "Gudang tidak ditemukan", 404

    # 🧼 nama file aman
    gudang_name = safe_filename(gudang_azka['nama_azka'])

    # 📁 folder
    base_dir = os.path.join(
        current_app.root_path,
        'static',
        'qr_gudang_azka',
        f'gudang_{warehouse_id}'
    )
    os.makedirs(base_dir, exist_ok=True)

    # 🖼️ file path pakai nama gudang
    qr_path = os.path.join(base_dir, f'{gudang_name}.png')

    # ⚙️ generate QR jika belum ada
    if not os.path.exists(qr_path):
        qr = qrcode.make(gudang_azka['qr_code_data_azka'])
        qr.save(qr_path)

    return send_file(qr_path, mimetype='image/png')
@app.route('/gudang_add_azka', methods=['POST'])
def gudang_add_azka():
    nama_azka = request.form['nama_azka']
    address_azka = request.form['address_azka']

    # 🌍 Geocoding alamat gudang
    lat, lng = get_lat_lng_from_address(address_azka)

    # ❌ jika gagal dapat koordinat
    if lat is None or lng is None:
        flash(
            "❌ Alamat gudang tidak ditemukan di peta. "
            "Mohon gunakan alamat yang lebih lengkap.",
            "warning"
        )
        return redirect(url_for('gudang_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_warehouses_azka
        (nama_azka, address_azka, latitude_azka, longitude_azka)
        VALUES (%s, %s, %s, %s)
    """, (nama_azka, address_azka, lat, lng))
    conn.commit()

    id_azka = cursor.lastrowid
    qr_data_azka = f"GUDANG|{id_azka}"

    cursor.execute("""
        UPDATE tbl_warehouses_azka
        SET qr_code_data_azka = %s
        WHERE id_azka = %s
    """, (qr_data_azka, id_azka))

    conn.commit()
    conn.close()

    insert_log_azka(
        session['user_id_azka'],
        "Tambah Data",
        f"Gudang #{nama_azka} ditambahkan"
    )

    flash("Gudang berhasil ditambahkan + lokasi otomatis 📍", "success")
    return redirect(url_for('gudang_azka'))


@app.route('/gudang_edit_azka/<int:id_azka>', methods=['POST'])
def gudang_edit_azka(id_azka):

    nama_azka = request.form['nama_azka']
    address_azka = request.form['address_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_warehouses_azka
        SET nama_azka=%s,
            address_azka=%s
        WHERE id_azka=%s
    """, (nama_azka, address_azka,id_azka))

    conn.commit()
    conn.close()

    flash("gudang berhasil diupdate!", "success")
    return redirect('/gudang_azka')
@app.route('/gudang_delete_azka/<int:id>')
def gudang_delete_azka(id):
    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # 🔍 cek relasi shipment
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tbl_shipment_azka
        WHERE warehouse_id_azka = %s
    """, (id,))
    shipment_count = cursor.fetchone()['total']

    # 🔍 cek relasi scan kurir (jika tabel ada)
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tbl_courier_scans_azka
        WHERE warehouse_id_azka = %s
    """, (id,))
    scan_count = cursor.fetchone()['total']

    if shipment_count > 0 or scan_count > 0:
        conn.close()
        flash(
            f"❌ Gudang tidak bisa dihapus! "
            f"Masih terhubung dengan {shipment_count} shipment "
            f"dan {scan_count} riwayat scan.",
            "warning"
        )
        return redirect(url_for('gudang_azka'))

    # ✅ aman untuk dihapus
    cursor.execute("""
        DELETE FROM tbl_warehouses_azka
        WHERE id_azka = %s
    """, (id,))

    conn.commit()
    conn.close()

    flash("✅ Gudang berhasil dihapus", "success")
    return redirect(url_for('gudang_azka'))



@app.route('/qr_paket_azka/<tracking>')
def qr_paket_azka(tracking):
    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT qr_token_azka
        FROM tbl_shipment_azka
        WHERE tracking_number_azka=%s
    """, (tracking,))
    s = cursor.fetchone()
    conn.close()

    if not s:
        return "Paket tidak ditemukan", 404

    qr_data = f"PAKET|{s['qr_token_azka']}"

    qr = qrcode.make(qr_data)
    img = BytesIO()
    qr.save(img, 'PNG')
    img.seek(0)

    return send_file(img, mimetype='image/png')
@app.route('/shipment_azka')
def shipment_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # ===== DATA SHIPMENT =====
    cursor.execute("""
        SELECT
            s.id_azka,
            s.tracking_number_azka,
            s.sender_name_azka,
            s.receiver_name_azka,
            s.receiver_address_azka,
            s.status_azka,
            s.created_at_azka,
            s.destination_lat,
            s.destination_lng,
            s.origin_lat,
            s.origin_lng,
            s.qr_code_data_azka,
            u.username_azka AS courier,
            w.nama_azka AS origin_name
        FROM tbl_shipment_azka s
        LEFT JOIN tbl_users_azka u
            ON s.courier_id_azka = u.id_azka
        LEFT JOIN tbl_warehouses_azka w
            ON s.warehouse_id_azka = w.id_azka
        ORDER BY s.created_at_azka DESC
    """)
    shipments = cursor.fetchall()

    # ===== AMBIL SEMUA GUDANG SEBAGAI HUB =====
    cursor.execute("""
        SELECT id_azka, nama_azka, latitude_azka, longitude_azka
        FROM tbl_warehouses_azka
        WHERE latitude_azka IS NOT NULL AND longitude_azka IS NOT NULL
        ORDER BY id_azka ASC
    """)
    all_hubs = cursor.fetchall()

    # ===== BUILD ROUTES =====
    for s in shipments:
        routes = []

        # ORIGIN
        if s['origin_lat'] and s['origin_lng']:
            routes.append({
                "lat": s['origin_lat'],
                "lng": s['origin_lng'],
                "name": s['origin_name'],
                "type": "ORIGIN"
            })
# ===== PILIH HUB TERDEKAT DARI TUJUAN =====
        nearest_hub = None
        nearest_distance = None

        for h in all_hubs:
            # skip gudang asal
            if (
                h['latitude_azka'] == s['origin_lat'] and
                h['longitude_azka'] == s['origin_lng']
            ):
                continue

            dist = haversine(
                s['destination_lat'],
                s['destination_lng'],
                h['latitude_azka'],
                h['longitude_azka']
            )

            if nearest_distance is None or dist < nearest_distance:
                nearest_distance = dist
                nearest_hub = h

        # ===== TAMBAHKAN HUB TERPILIH =====
        if nearest_hub:
            routes.append({
                "lat": nearest_hub['latitude_azka'],
                "lng": nearest_hub['longitude_azka'],
                "name": nearest_hub['nama_azka'],
                "type": "HUB"
            })


        # DESTINATION
        if s['destination_lat'] and s['destination_lng']:
            routes.append({
                "lat": s['destination_lat'],
                "lng": s['destination_lng'],
                "name": s['receiver_name_azka'],
                "type": "DESTINATION"
            })

        s['routes'] = routes

        # POSISI TRUCK
        if s['status_azka'] != 'CREATED' and routes:
            s['truck_position'] = {
                "lat": routes[0]['lat'],
                "lng": routes[0]['lng']
            }
        else:
            s['truck_position'] = None

        # FIX QR
        if not s['qr_code_data_azka']:
            s['qr_code_data_azka'] = f"PAKET|{s['id_azka']}|{s['tracking_number_azka']}"

    # ===== DATA GUDANG (DROPDOWN) =====
    cursor.execute("""
        SELECT id_azka, nama_azka
        FROM tbl_warehouses_azka
        ORDER BY nama_azka ASC
    """)
    warehouses_azka = cursor.fetchall()

    conn.close()

    return render_template(
        'shipment_azka.html',
        data_shipment_azka=shipments,
        warehouses_azka=warehouses_azka,
        username_azka=session['username_azka']
    )
@app.route('/shipment_add_azka', methods=['POST'])
def shipment_add_azka():

    tracking_number = f"AE-{int(time.time())}-{random.randint(100,999)}"
    warehouse_id = request.form['warehouse_id_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    try:
        conn.start_transaction()

        # ===== ORIGIN (GUDANG) =====
        cursor.execute("""
            SELECT latitude_azka, longitude_azka
            FROM tbl_warehouses_azka
            WHERE id_azka=%s
        """, (warehouse_id,))
        wh = cursor.fetchone()

        if not wh:
            raise Exception("Gudang tidak ditemukan")

        origin_lat = wh['latitude_azka']
        origin_lng = wh['longitude_azka']

        # ===== DESTINATION =====
        receiver_address = request.form['receiver_address_azka']
        dest_lat, dest_lng, dest_city = get_lat_lng_city_from_address(receiver_address)

        if not dest_lat or not dest_lng:
            raise Exception("Alamat tujuan tidak ditemukan")

        # ===== INSERT SHIPMENT =====
        cursor.execute("""
            INSERT INTO tbl_shipment_azka
            (tracking_number_azka, sender_name_azka, receiver_name_azka,
             receiver_address_azka, receiver_city_azka,
             warehouse_id_azka,
             origin_lat, origin_lng,
             destination_lat, destination_lng,
             last_lat, last_lng,
             status_azka)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'CREATED')
        """, (
            tracking_number,
            request.form['sender_name_azka'],
            request.form['receiver_name_azka'],
            receiver_address,
            dest_city,
            warehouse_id,
            origin_lat, origin_lng,
            dest_lat, dest_lng,
            origin_lat, origin_lng
        ))

        shipment_id = cursor.lastrowid

        # ===== QR DATA =====
        qr_data = f"PAKET|{shipment_id}|{tracking_number}"

        cursor.execute("""
            UPDATE tbl_shipment_azka
            SET qr_code_data_azka=%s
            WHERE id_azka=%s
        """, (qr_data, shipment_id))

        # ===== GENERATE QR FILE =====
        qr_folder = "static/qr_paket"
        os.makedirs(qr_folder, exist_ok=True)

        qr_img = qrcode.make(qr_data)
        qr_path = f"{qr_folder}/{tracking_number}.png"
        qr_img.save(qr_path)

        # ===== INSERT BARANG =====
        cursor.execute("""
            INSERT INTO tbl_products_azka
            (shipment_id_azka, nama_barang_azka, berat_azka, qty_azka)
            VALUES (%s,%s,%s,%s)
        """, (
            shipment_id,
            request.form['nama_barang_azka'],
            request.form['berat_azka'],
            request.form['qty_azka']
        ))

        # ✅ SEMUA SUKSES
        conn.commit()
        flash("Shipment + QR paket berhasil dibuat 📦", "success")

    except Exception as e:
        conn.rollback()
        print("TRANSACTION ERROR:", e)
        flash(str(e), "danger")

    finally:
        conn.close()

    return redirect(url_for('shipment_azka'))

@app.route('/shipment_delete_azka/<int:shipment_id>', methods=['POST'])
def shipment_delete_azka(shipment_id):

    if 'user_id_azka' not in session:
        return "Unauthorized", 401

    # 🔒 HANYA ADMIN
    if session.get('role_id_azka') != 1:
        return "Forbidden", 403

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # ===== AMBIL SHIPMENT =====
    cursor.execute("""
        SELECT status_azka
        FROM tbl_shipment_azka
        WHERE id_azka = %s
    """, (shipment_id,))
    shipment = cursor.fetchone()

    if not shipment:
        conn.close()
        flash("Shipment tidak ditemukan", "danger")
        return redirect(url_for('shipment_azka'))

    # 🚫 STATUS YANG TIDAK BOLEH DIHAPUS
    forbidden_status = [
        'PICKUP',
        'ARRIVED_AT_ORIGIN_HUB',
        'IN_TRANSIT',
        'SORTING',
        'OUT_FOR_DELIVERY',
        'ON_THE_WAY',
        'DELIVERED'
    ]

    if shipment['status_azka'] in forbidden_status:
        conn.close()
        flash("Shipment sudah diproses, tidak bisa dihapus ❌", "danger")
        return redirect(url_for('shipment_azka'))

    # ===== HAPUS DATA TERKAIT (AMAN) =====
    cursor.execute("DELETE FROM tbl_products_azka WHERE shipment_id_azka=%s", (shipment_id,))
    cursor.execute("DELETE FROM tbl_courier_scans_azka WHERE shipment_id_azka=%s", (shipment_id,))
    cursor.execute("DELETE FROM tbl_driver_scans_azka WHERE shipment_id_azka=%s", (shipment_id,))

    # ===== HAPUS SHIPMENT =====
    cursor.execute("DELETE FROM tbl_shipment_azka WHERE id_azka=%s", (shipment_id,))

    # ===== LOG =====
    cursor.execute("""
        INSERT INTO tbl_activity_logs_azka
        (user_id_azka, actions_azka, created_at_azka)
        VALUES (%s,%s,NOW())
    """, (
        session['user_id_azka'],
        f"Hapus shipment ID {shipment_id}"
    ))

    conn.commit()
    conn.close()

    flash("Shipment berhasil dihapus 🗑️", "success")
    return redirect(url_for('shipment_azka'))

# ===========================
#   GUDANG DASHBOARD
# ===========================

@app.route('/gudang_dashboard_azka')
def gudang_dashboard_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in (1, 2):
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # ================= SHIPMENT SORTING (INTI) =================
    cursor.execute("""
        SELECT
            tracking_number_azka,
            receiver_name_azka,
            receiver_address_azka,
            receiver_city_azka,
            status_azka,
            updated_at_azka
        FROM tbl_shipment_azka
        WHERE status_azka = 'SORTING'
        ORDER BY receiver_city_azka ASC, updated_at_azka DESC
    """)
    rows = cursor.fetchall()

    # 🔥 GROUP BY KOTA
    data_per_kota = defaultdict(list)
    for r in rows:
        kota = r['receiver_city_azka'] or 'TIDAK DIKETAHUI'
        data_per_kota[kota].append(r)

    # ================= SHIPMENT DALAM PERJALANAN =================
    cursor.execute("""
        SELECT id_azka, tracking_number_azka, status_azka
        FROM tbl_shipment_azka
        WHERE status_azka IN ('IN_TRANSIT', 'ARRIVED_AT_DEST_HUB')
    """)
    shipment_scan_list_azka = cursor.fetchall()

    conn.close()

    return render_template(
        'gudang_dashboard_azka.html',
        username_azka=session['username_azka'],
        data_per_kota=data_per_kota,            # ✅ PENTING
        shipment_scan_list_azka=shipment_scan_list_azka
    )
@app.route('/scan_sortir_azka', methods=['POST'])
def scan_sortir_azka():
    data = request.get_json()
    raw_qr = data.get('tracking_number')

    if not raw_qr:
        return jsonify({"status": "danger", "message": "❌ QR kosong"})

    # ================= PARSE QR =================
    # Format: PAKET|shipment_id|tracking_number
    parts = raw_qr.strip().split("|")
    if len(parts) != 3 or parts[0] != "PAKET":
        return jsonify({
            "status": "danger",
            "message": "❌ Format QR tidak valid"
        })

    shipment_id = int(parts[1])
    tracking = parts[2]

    conn = get_db_connection_azka()
    conn.autocommit = False
    cursor = conn.cursor(dictionary=True)

    # 🔒 Lock shipment (anti double scan)
    cursor.execute("""
        SELECT id_azka, status_azka
        FROM tbl_shipment_azka
        WHERE id_azka=%s AND tracking_number_azka=%s
        FOR UPDATE
    """, (shipment_id, tracking))

    shipment = cursor.fetchone()
    if not shipment:
        conn.close()
        return jsonify({
            "status": "danger",
            "message": "❌ Paket tidak ditemukan"
        })

    # ================= VALIDASI STATUS =================
    if shipment['status_azka'] == 'SORTING':
        conn.close()
        return jsonify({
            "status": "warning",
            "message": "⚠️ Paket sudah dalam proses sortir"
        })

    if shipment['status_azka'] != 'IN_TRANSIT':
        conn.close()
        return jsonify({
            "status": "danger",
            "message": "❌ Paket belum siap disortir"
        })

    # ================= UPDATE =================
    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka='SORTING'
        WHERE id_azka=%s
    """, (shipment_id,))

    # 📝 ACTIVITY LOG
    cursor.execute("""
        INSERT INTO tbl_activity_logs_azka
        (user_id_azka, actions_azka, created_at_azka)
        VALUES (%s,%s,NOW())
    """, (
        session.get('user_id_azka'),
        f"📦 Paket masuk sortir | {tracking}"
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "✅ Paket berhasil masuk proses sortir",
        "reload": True
    })

@app.route('/scan_kurir_ready_delivery_azka', methods=['POST'])
def scan_kurir_ready_delivery_azka():
    data = request.get_json()

    qr_kurir = data.get('qr_kurir')
    qr_paket = data.get('qr_paket')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not qr_kurir or not qr_paket:
        return jsonify({
            "status": "danger",
            "message": "❌ QR kurir & paket wajib discan"
        })

    # ================= PARSE QR =================
    try:
        k = qr_kurir.split("|")
        p = qr_paket.split("|")

        if k[0] != "KURIR" or p[0] != "PAKET":
            raise ValueError

        courier_id = int(k[1])
        shipment_id = int(p[1])
        tracking = p[2]

    except Exception:
        return jsonify({
            "status": "danger",
            "message": "❌ Format QR tidak valid"
        })
    print("SESSION:", dict(session))
    warehouse_id = session.get('warehouse_id_azka')
    user_id = session.get('user_id_azka')
    if not warehouse_id or not user_id:
        return jsonify({
            "status": "danger",
            "message": f"❌ Session gudang tidak valid | session={dict(session)}"
        })

    conn = get_db_connection_azka()
    conn.autocommit = False
    cursor = conn.cursor(dictionary=True)

    # 🔒 Lock shipment
    cursor.execute("""
        SELECT id_azka, status_azka, courier_id_azka
        FROM tbl_shipment_azka
        WHERE id_azka=%s
        FOR UPDATE
    """, (shipment_id,))

    shipment = cursor.fetchone()
    if not shipment:
        conn.close()
        return jsonify({
            "status": "danger",
            "message": "❌ Paket tidak ditemukan"
        })

    if shipment['status_azka'] != 'SORTING':
        conn.close()
        return jsonify({
            "status": "warning",
            "message": "⚠️ Paket belum siap dilepas ke kurir"
        })

    if shipment['courier_id_azka'] is not None:
        conn.close()
        return jsonify({
            "status": "danger",
            "message": "❌ Paket sudah pernah diserahkan ke kurir"
        })

    # ================= SIMPAN SCAN =================
    cursor.execute("""
        INSERT INTO tbl_courier_scans_azka
        (courier_id_azka, shipment_id_azka, warehouse_id_azka,
         scan_type_azka, latitude_azka, longitude_azka)
        VALUES (%s,%s,%s,'OUT',%s,%s)
    """, (
        courier_id,
        shipment_id,
        warehouse_id,
        latitude,
        longitude
    ))

    # ================= UPDATE SHIPMENT =================
    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET
            status_azka='READY_FOR_DELIVERY',
            courier_id_azka=%s
        WHERE id_azka=%s
    """, (courier_id, shipment_id))

    # 📝 ACTIVITY LOG
    cursor.execute("""
        INSERT INTO tbl_activity_logs_azka
        (user_id_azka, actions_azka, created_at_azka)
        VALUES (%s,%s,NOW())
    """, (
        user_id,
        f"🚚 Paket {tracking} diserahkan ke kurir ID {courier_id}"
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "✅ Paket diserahkan ke kurir & siap dikirim"
    })

@app.route('/gudang_lokasi_azka')
def gudang_lokasi_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in (1, 2):

        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_azka, code_azka, description_azka
        FROM tbl_locations_azka
    """)

    lokasi_azka = cursor.fetchall()
    conn.close()

    return render_template("gudang_lokasi_azka.html",
                           username_azka=session['username_azka'],
                           lokasi_azka=lokasi_azka)

@app.route('/gudang_locations_add_azka', methods=['POST'])
def gudang_locations_add_azka():
    code_azka = request.form['code_azka']
    type_azka = request.form['type_azka']
    description_azka = request.form['description_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_locations_azka 
        (code_azka, type_azka, description_azka)
        VALUES (%s, %s, %s)
    """, (code_azka, type_azka, description_azka))

    conn.commit()
    conn.close()

    flash("Data Stock berhasil ditambahkan!", "success")
    return redirect('/gudang_lokasi_azka')



# ===========================
#   MANAGER DASHBOARD
# ===========================
# ---------------------------
# MANAGER: 1) Dashboard (expanded)
# ---------------------------
@app.route('/manager_dashboard_azka')
def manager_dashboard_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in [1, 4]:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # Statistik utama
    cursor.execute("SELECT COUNT(*) AS total_orders_today FROM tbl_orders_azka WHERE DATE(created_at_azka)=CURDATE()")
    total_orders_today = cursor.fetchone()['total_orders_today']

    cursor.execute("SELECT COUNT(*) AS in_transit FROM tbl_shipment_azka WHERE status_azka='in_transit'")
    in_transit = cursor.fetchone()['in_transit']

    cursor.execute("SELECT COUNT(*) AS delivered FROM tbl_shipment_azka WHERE status_azka='delivered'")
    delivered = cursor.fetchone()['delivered']

    cursor.execute("SELECT COUNT(*) AS failed FROM tbl_shipment_azka WHERE status_azka='failed'")
    failed = cursor.fetchone()['failed']

    cursor.execute("SELECT COUNT(*) AS total_receiving_today FROM tbl_receiving_azka WHERE DATE(created_at_azka)=CURDATE()")
    total_receiving_today = cursor.fetchone()['total_receiving_today']

    cursor.execute("SELECT COUNT(*) AS total_outbound_today FROM tbl_stock_movements_azka WHERE type_azka='outbound' AND DATE(created_at_azka)=CURDATE()")
    total_outbound_today = cursor.fetchone()['total_outbound_today']

    conn.close()

    return render_template(
        "manager_dashboard_azka.html",
        username_azka=session['username_azka'],
        total_orders_today=total_orders_today,
        in_transit=in_transit,
        delivered=delivered,
        failed=failed,
        total_receiving_today=total_receiving_today,
        total_outbound_today=total_outbound_today
    )


# ---------------------------
# 2) Shipment Control - lihat & assign / reassign kurir
# ---------------------------
@app.route('/manager_shipment_control_azka')
def manager_shipment_control_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in [1, 4]:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # Ambil shipment
    cursor.execute("""
        SELECT s.*, o.order_number_azka, o.customer_nama_azka, o.customer_addres_azka,
               o.created_at_azka, u.username_azka AS courier_name
        FROM tbl_shipment_azka s
        LEFT JOIN tbl_orders_azka o ON o.id_azka = s.order_id_azka
        LEFT JOIN tbl_users_azka u ON u.id_azka = s.kurir_id_azka
        ORDER BY s.id_azka DESC
        LIMIT 200
    """)
    shipments = cursor.fetchall()

    # Ambil kurir
    cursor.execute("SELECT id_azka, username_azka FROM tbl_users_azka WHERE role_id_azka=3")
    couriers = cursor.fetchall()

    conn.close()

    return render_template(
        "manager_shipment_control_azka.html",
        username_azka=session['username_azka'],
        shipments=shipments,
        couriers=couriers
    )

@app.route('/manager_assign_courier_azka/<int:shipment_id>', methods=['POST'])
def manager_assign_courier_azka(shipment_id):
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session['role_id_azka'] not in [1, 4]:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    courier_id = request.form.get('courier_id')

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_shipment_azka 
        SET kurir_id_azka=%s 
        WHERE id_azka=%s
    """, (courier_id, shipment_id))

    conn.commit()
    conn.close()

    flash("Kurir berhasil di-assign!", "success")
    return redirect(url_for('manager_shipment_control_azka'))

# ---------------------------
# 4) Courier Performance (leaderboard)
# ---------------------------
@app.route('/manager_courier_performance_azka')
def manager_courier_performance_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in [1, 4]:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # Hitung delivered & failed per kurir dari tbl_shipment_azka (join kurir_id_azka)
    cursor.execute("""
        SELECT u.id_azka AS courier_id, u.username_azka AS courier_name,
               SUM(CASE WHEN s.status_azka='delivered' THEN 1 ELSE 0 END) AS total_delivered,
               SUM(CASE WHEN s.status_azka='failed' THEN 1 ELSE 0 END) AS total_failed,
               COUNT(s.id_azka) AS total_assigned
        FROM tbl_users_azka u
        LEFT JOIN tbl_shipment_azka s ON s.kurir_id_azka = u.id_azka
        WHERE u.role_id_azka = 3
        GROUP BY u.id_azka, u.username_azka
        ORDER BY total_delivered DESC
    """)
    performance = cursor.fetchall()
    conn.close()

    return render_template("manager_courier_performance_azka.html",
                           username_azka=session['username_azka'],
                           performance=performance)


# ---------------------------
# 5) Activity Logs (filterable)
# ---------------------------
@app.route('/manager_activity_logs_azka')
def manager_activity_logs_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in [1, 4]:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    q_user = request.args.get('user_id')
    q_from = request.args.get('from')
    q_to = request.args.get('to')

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    base_q = "SELECT a.*, u.username_azka FROM tbl_activity_logs_azka a LEFT JOIN tbl_users_azka u ON u.id_azka=a.user_id_azka WHERE 1=1"
    params = []
    if q_user:
        base_q += " AND a.user_id_azka=%s"
        params.append(q_user)
    if q_from:
        base_q += " AND DATE(a.created_at_azka) >= %s"
        params.append(q_from)
    if q_to:
        base_q += " AND DATE(a.created_at_azka) <= %s"
        params.append(q_to)

    base_q += " ORDER BY a.created_at_azka DESC LIMIT 500"
    cursor.execute(base_q, tuple(params))
    logs = cursor.fetchall()

    # untuk dropdown user filter
    cursor.execute("SELECT id_azka, username_azka FROM tbl_users_azka")
    users = cursor.fetchall()

    conn.close()
    return render_template("manager_activity_logs_azka.html",
                           username_azka=session['username_azka'],
                           logs=logs, users=users)


# ---------------------------
# 6) Area Report - distribusi per kota / area
# ---------------------------
@app.route('/manager_area_report_azka')
def manager_area_report_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in [1, 4]:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    # Ambil aggregasi berdasarkan customer_addres_azka (kamu bisa menyesuaikan parsing kota)
    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            SUBSTRING_INDEX(customer_addres_azka, '-', -1) AS kota, 
            COUNT(o.id_azka) AS total_orders,
            SUM(CASE WHEN s.status_azka='delivered' THEN 1 ELSE 0 END) AS delivered,
            SUM(CASE WHEN s.status_azka='failed' THEN 1 ELSE 0 END) AS failed
        FROM tbl_orders_azka o
        LEFT JOIN tbl_shipment_azka s ON s.order_id_azka = o.id_azka
        GROUP BY kota
        ORDER BY total_orders DESC
        LIMIT 100
    """)
    per_area = cursor.fetchall()
    conn.close()

    return render_template("manager_area_report_azka.html",
                           username_azka=session['username_azka'],
                           per_area=per_area)



@app.route('/manager_po_monitor_azka')
def manager_po_monitor_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in [1, 4]:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.*, s.nama_azka AS supplier_name
        FROM tbl_purchase_orders_azka p
        LEFT JOIN tbl_suppliers_azka s ON s.id_azka = p.supplier_id_azka
        ORDER BY p.created_at_azka DESC
        LIMIT 200
    """)
    pos = cursor.fetchall()
    conn.close()

    return render_template("manager_po_monitor_azka.html",
                           username_azka=session['username_azka'],
                           pos=pos)
@app.route('/kurir_dashboard_azka')
def kurir_dashboard_azka():
    if 'user_id_azka' not in session:
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') != 3:
        flash("Akses ditolak", "danger")
        return redirect(url_for('dashboard_azka'))

    conn_azka = get_db_connection_azka()
    cursor_azka = conn_azka.cursor(dictionary=True)

    # Data kurir
    cursor_azka.execute("""
        SELECT id_azka, username_azka
        FROM tbl_users_azka
        WHERE id_azka = %s
    """, (session['user_id_azka'],))
    kurir_azka = cursor_azka.fetchone()

    # Scan terakhir kurir
    cursor_azka.execute("""
        SELECT cs.*, w.namA_azka
        FROM tbl_courier_scans_azka cs
        LEFT JOIN tbl_warehouses_azka w 
            ON cs.warehouse_id_azka = w.id_azka
        WHERE cs.courier_id_azka = %s
        ORDER BY cs.scan_time_azka DESC
        LIMIT 1
    """, (session['user_id_azka'],))
    last_scan_azka = cursor_azka.fetchone()

    conn_azka.close()

    return render_template(
        'kurir_dashboard_azka.html',
        kurir_azka=kurir_azka,
        last_scan_azka=last_scan_azka
    )

@app.route('/qr_kurir_azka/<int:courier_id_azka>')
def qr_kurir_azka(courier_id_azka):
    if 'user_id_azka' not in session:
        return redirect(url_for('login_azka'))

    conn_azka = get_db_connection_azka()
    cursor_azka = conn_azka.cursor(dictionary=True)

    cursor_azka.execute("""
        SELECT id_azka, username_azka
        FROM tbl_users_azka
        WHERE id_azka = %s AND role_id_azka = 3
    """, (courier_id_azka,))
    kurir_azka = cursor_azka.fetchone()
    conn_azka.close()

    if not kurir_azka:
        return "Kurir tidak ditemukan", 404

    qr_data_azka = f"KURIR|{kurir_azka['id_azka']}|{kurir_azka['username_azka']}"

    qr_azka = qrcode.make(qr_data_azka)

    folder_azka = "static/qr_kurir"
    os.makedirs(folder_azka, exist_ok=True)

    file_path_azka = f"{folder_azka}/kurir_{kurir_azka['id_azka']}.png"
    qr_azka.save(file_path_azka)

    return send_file(file_path_azka, mimetype='image/png')
@app.route('/scan_kurir_azka', methods=['POST'])
def scan_kurir_azka():
    if 'user_id_azka' not in session:
        return "Unauthorized", 401
    if session.get('role_id_azka') != 3:
        return "Forbidden", 403

    courier_id = session['user_id_azka']
    scan_type = request.form.get('scan_type_azka')
    warehouse_id = request.form.get('warehouse_id_azka')
    package_code = request.form.get('package_code')

    conn = get_db_connection_azka()
    conn.autocommit = False
    cursor = conn.cursor(dictionary=True)

    # 1️⃣ SHIPMENT AKTIF KURIR
    cursor.execute("""
        SELECT *
        FROM tbl_shipment_azka
        WHERE courier_id_azka=%s
          AND status_azka!='DELIVERED'
        LIMIT 1
        FOR UPDATE
    """, (courier_id,))
    shipment = cursor.fetchone()

    if not shipment:
        conn.close()
        return "Tidak ada shipment aktif", 400

    status = shipment['status_azka']
    new_status = None

    # ================== FLOW FINAL ==================

    # Kurir ambil paket dari hub
    if status == 'READY_FOR_DELIVERY' and scan_type == 'OUT':
        if not warehouse_id:
            conn.close()
            return "Scan gudang wajib", 400
        new_status = 'ON_THE_WAY'

    # Kurir scan QR paket ke penerima
    elif status == 'ON_THE_WAY' and scan_type == 'PACKAGE':
        if not package_code:
            conn.close()
            return "QR paket tidak valid", 400

        if package_code != shipment['tracking_number_azka']:
            conn.close()
            return "QR paket tidak sesuai shipment", 400

        new_status = 'DELIVERED'
        cursor.execute("""
            UPDATE tbl_shipment_azka
            SET courier_id_azka = NULL
            WHERE id_azka = %s
        """, (shipment['id_azka'],))

    else:
        conn.close()
        return f"Scan tidak valid ({status} + {scan_type})", 400

    # ================== UPDATE SHIPMENT ==================
    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka=%s
        WHERE id_azka=%s
    """, (new_status, shipment['id_azka']))

    # ================== LOG ==================
    cursor.execute("""
        INSERT INTO tbl_courier_scans_azka
        (shipment_id_azka, courier_id_azka, scan_type_azka, scan_time_azka)
        VALUES (%s,%s,%s,NOW())
    """, (
        shipment['id_azka'],
        courier_id,
        scan_type
    ))

    conn.commit()
    conn.close()
    return "OK"


@app.route('/scan_kurir_masuk_gudang_azka', methods=['POST'])
def scan_kurir_masuk_gudang_azka():

    if 'user_id_azka' not in session:
        return 'Unauthorized', 401

    qr_data = request.form.get('qr_data_azka')
    if not qr_data:
        return 'QR tidak terbaca', 400

    # 🔍 PARSE QR → KURIR|id|username
    try:
        prefix, kurir_id, kurir_username = qr_data.split('|')
        if prefix != 'KURIR':
            return 'QR tidak valid', 400
    except:
        return 'Format QR salah', 400

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    try:
        # ✅ CEK KURIR (USER ROLE = 3)
        cursor.execute("""
            SELECT id_azka, username_azka
            FROM tbl_users_azka
            WHERE id_azka = %s AND role_id_azka = 3
        """, (kurir_id,))
        kurir = cursor.fetchone()

        if not kurir:
            return 'Kurir tidak ditemukan', 404

        # ✅ SIMPAN LOG MASUK GUDANG
        cursor.execute("""
            INSERT INTO tbl_scan_kurir_masuk_gudang_azka
            (kurir_id_azka, waktu_scan_azka, status_scan_azka, keterangan_azka)
            VALUES (%s, NOW(), 'masuk', 'Scan QR Kurir')
        """, (kurir['id_azka'],))

        conn.commit()

        return f"Kurir {kurir['username_azka']} berhasil masuk gudang", 200

    except Exception as e:
        conn.rollback()
        return f"Server error: {str(e)}", 500

    finally:
        cursor.close()
        conn.close()

@app.route('/qr_sopir_azka/<int:driver_id_azka>')
def qr_sopir_azka(driver_id_azka):

    if 'user_id_azka' not in session:
        return redirect(url_for('login_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_azka, username_azka
        FROM tbl_users_azka
        WHERE id_azka=%s AND role_id_azka=5
    """, (driver_id_azka,))

    sopir = cursor.fetchone()
    conn.close()

    if not sopir:
        return "Sopir tidak ditemukan", 404

    qr_data = f"SOPIR|{sopir['id_azka']}|{sopir['username_azka']}"

    qr = qrcode.make(qr_data)

    folder = "static/qr_sopir"
    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/sopir_{sopir['id_azka']}.png"
    qr.save(file_path)

    return send_file(file_path, mimetype='image/png')
@app.route('/scan_sopir_azka', methods=['POST'])
def scan_sopir_azka():

    if 'user_id_azka' not in session:
        return "Unauthorized", 401

    if session.get('role_id_azka') != 5:
        return "Forbidden", 403

    driver_id = session['user_id_azka']
    scan_type = request.form.get('scan_type_azka')
    warehouse_id = request.form.get('warehouse_id_azka')

    if scan_type not in ['IN', 'OUT']:
        return "Scan wajib IN atau OUT", 400

    if not warehouse_id:
        return "Warehouse wajib", 400

    warehouse_id = int(warehouse_id)

    conn = get_db_connection_azka()
    conn.autocommit = False
    cursor = conn.cursor(dictionary=True)

    # 🔍 Scan terakhir driver
    cursor.execute("""
        SELECT scan_type_azka
        FROM tbl_driver_scans_azka
        WHERE driver_id_azka=%s
        ORDER BY scan_time_azka DESC
        LIMIT 1
    """, (driver_id,))
    last_scan = cursor.fetchone()

    # 🔒 Validasi urutan scan
    if not last_scan and scan_type != 'IN':
        conn.close()
        return "Scan pertama wajib IN", 400

    if last_scan and scan_type == last_scan['scan_type_azka']:
        conn.close()
        return "Urutan scan tidak valid", 400

    # 📦 Shipment aktif
    cursor.execute("""
        SELECT *
        FROM tbl_shipment_azka
        WHERE driver_id_azka=%s
          AND status_azka!='DELIVERED'
        LIMIT 1
        FOR UPDATE
    """, (driver_id,))
    shipment = cursor.fetchone()

    # 🆕 Assign shipment saat scan IN pertama
    if not shipment:
        if scan_type != 'IN':
            conn.close()
            return "Harus scan IN terlebih dahulu", 400

        cursor.execute("""
            SELECT *
            FROM tbl_shipment_azka
            WHERE driver_id_azka IS NULL
              AND status_azka='CREATED'
              AND warehouse_id_azka=%s
            ORDER BY created_at_azka ASC
            LIMIT 1
            FOR UPDATE
        """, (warehouse_id,))
        shipment = cursor.fetchone()

        if not shipment:
            conn.close()
            return "Tidak ada shipment tersedia", 400

        cursor.execute("""
            UPDATE tbl_shipment_azka
            SET driver_id_azka=%s
            WHERE id_azka=%s
        """, (driver_id, shipment['id_azka']))

    # 🏭 Data gudang
    cursor.execute("""
        SELECT nama_azka, latitude_azka, longitude_azka
        FROM tbl_warehouses_azka
        WHERE id_azka=%s
    """, (warehouse_id,))
    wh = cursor.fetchone()

    status = shipment['status_azka']
    new_status = None

    # 🔁 ALUR STATUS FINAL
    if status == 'CREATED' and scan_type == 'IN':
        new_status = 'PICKUP'

    elif status == 'PICKUP' and scan_type == 'OUT':
        new_status = 'ARRIVED_AT_ORIGIN_HUB'

    elif status == 'ARRIVED_AT_ORIGIN_HUB' and scan_type == 'IN':
        new_status = 'IN_TRANSIT'

    elif status == 'IN_TRANSIT' and scan_type == 'IN':
        new_status = 'SORTING'

    elif status == 'SORTING' and scan_type == 'IN':
        new_status = 'READY_FOR_DELIVERY'
        cursor.execute("""
            UPDATE tbl_shipment_azka
            SET driver_id_azka=NULL
            WHERE id_azka=%s
        """, (shipment['id_azka'],))

    else:
        conn.close()
        return "Scan tidak sesuai alur", 400

    # 🔄 Update shipment
    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka=%s,
            warehouse_id_azka=%s
        WHERE id_azka=%s
    """, (new_status, warehouse_id, shipment['id_azka']))

    # 📝 Activity log
    description = get_description(
        new_status,
        wh['nama_azka'],
        shipment['is_interisland']
    )

    cursor.execute("""
        INSERT INTO tbl_driver_scans_azka
        (shipment_id_azka, driver_id_azka, warehouse_id_azka,
         scan_type_azka, latitude_azka, longitude_azka, scan_time_azka)
        VALUES (%s,%s,%s,%s,%s,%s,NOW())
    """, (
        shipment['id_azka'],
        driver_id,
        warehouse_id,
        scan_type,
        wh['latitude_azka'],
        wh['longitude_azka']
    ))

    cursor.execute("""
        INSERT INTO tbl_activity_logs_azka
        (user_id_azka, actions_azka, created_at_azka)
        VALUES (%s,%s,NOW())
    """, (
        driver_id,
        f"{description} | {shipment['tracking_number_azka']}"
    ))

    conn.commit()
    conn.close()
    return "OK"

@app.route('/dashboard_sopir_azka')
def dashboard_sopir_azka():
    if 'user_id_azka' not in session:
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') != 5:
        flash("Akses ditolak", "danger")
        return redirect(url_for('dashboard_azka'))

    conn_azka = get_db_connection_azka()
    cursor_azka = conn_azka.cursor(dictionary=True)

    # Data kurir
    cursor_azka.execute("""
        SELECT id_azka, username_azka
        FROM tbl_users_azka
        WHERE id_azka = %s
    """, (session['user_id_azka'],))
    kurir_azka = cursor_azka.fetchone()

    # Scan terakhir kurir
    cursor_azka.execute("""
        SELECT cs.*, w.namA_azka
        FROM tbl_driver_scans_azka cs
        LEFT JOIN tbl_warehouses_azka w 
            ON cs.warehouse_id_azka = w.id_azka
        WHERE cs.driver_id_azka = %s
        ORDER BY cs.scan_time_azka DESC
        LIMIT 1
    """, (session['user_id_azka'],))
    last_scan_azka = cursor_azka.fetchone()

    conn_azka.close()

    return render_template(
        'dashboard_sopir_azka.html',
        kurir_azka=kurir_azka,
        last_scan_azka=last_scan_azka
    )
@app.route('/logout_azka')
def logout_azka():
    if 'user_id_azka' in session:
        insert_log_azka(
            session['user_id_azka'],
            "Logout",
            f"User {session.get('username_azka')} berhasil logout"
        )


    session.clear()

    flash("Berhasil logout!", "success")
    return redirect(url_for('login_azka'))

if __name__ == "__main__":
    app.run(debug=True)
