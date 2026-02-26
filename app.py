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
@app.after_request
def disable_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

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
        return f"🚛 Paket sedang dalam perjalanan Ke {warehouse_name}"
    if status == 'TRANSIT_HUB':
        return f"🔄 Paket sedang transit di hub {warehouse_name}"

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

    # 🔒 JIKA SUDAH LOGIN, TIDAK BOLEH BALIK KE LOGIN
    if session.get('logged_in_azka'):
        return redirect(url_for('dashboard_azka'))

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
            WHERE username_azka = %s
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

        # 🔐 RESET SESSION TOTAL
        session.clear()

        # ✅ SESSION FINAL
        session['logged_in_azka'] = True
        session['user_id_azka'] = user_azka['id_azka']
        session['username_azka'] = user_azka['username_azka']
        session['role_id_azka'] = user_azka['role_id_azka']
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

    conn_azka = get_db_connection_azka()
    cursor_azka = conn_azka.cursor(dictionary=True)
    

    tables_azka = {
        "total_users_azka": "tbl_users_azka",
        "total_warehouses_azka": "tbl_warehouses_azka",
        "total_shipment_azka": "tbl_shipment_azka",
        "total_logs_azka": "tbl_activity_logs_azka",
        "total_barang_azka": "tbl_products_azka",
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
        SELECT COUNT(*) AS total_driver_azka
        FROM tbl_users_azka
        WHERE role_id_azka = 5
    """)
    total_driver_azka = cursor_azka.fetchone()['total_driver_azka']

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

    # ===================== LOG PAKET PER SHIPMENT (FINAL - NO DOUBLE) =====================
    cursor_azka.execute("""
    SELECT DISTINCT
        s.id_azka AS shipment_id_azka,
        s.tracking_number_azka,
        s.status_azka,

        u.username_azka AS nama_aktor_azka,

        CASE
            WHEN u.role_id_azka = 3 THEN 'KURIR'
            WHEN u.role_id_azka = 5 THEN 'DRIVER'
            WHEN u.role_id_azka = 2 THEN 'GUDANG'
            ELSE 'Administrator'
        END AS role_aktor_azka,

        CASE
            WHEN cs.scan_type_azka = 'OUT'
                THEN CONCAT('Paket ', s.tracking_number_azka, ' sedang dalam perjalanan')
            WHEN cs.scan_type_azka = 'IN'
                THEN CONCAT('Paket ', s.tracking_number_azka, ' tiba di gudang')
            ELSE l.actions_azka
        END AS deskripsi_azka,

        l.created_at_azka

    FROM tbl_activity_logs_azka l

    JOIN tbl_users_azka u
        ON l.user_id_azka = u.id_azka

    JOIN tbl_shipment_azka s
        ON l.actions_azka LIKE CONCAT('%', s.tracking_number_azka, '%')

    LEFT JOIN (
        SELECT cs1.*
        FROM tbl_courier_scans_azka cs1
        JOIN (
            SELECT courier_id_azka, MAX(scan_time_azka) AS last_scan
            FROM tbl_courier_scans_azka
            GROUP BY courier_id_azka
        ) last_cs
        ON cs1.courier_id_azka = last_cs.courier_id_azka
        AND cs1.scan_time_azka = last_cs.last_scan
    ) cs
    ON cs.courier_id_azka = u.id_azka

    WHERE l.actions_azka LIKE '%Paket%'

    ORDER BY l.created_at_azka DESC

    """)

    raw_logs_azka = cursor_azka.fetchall()


    # ================= GROUP PER SHIPMENT =================
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

        log_data = {
            "nama_aktor_azka": row['nama_aktor_azka'],
            "role_aktor_azka": row['role_aktor_azka'],
            "deskripsi_azka": row['deskripsi_azka'],
            "created_at_azka": row['created_at_azka']
        }

        # Anti double
        if log_data not in shipment_logs_azka[sid]["logs"]:
            shipment_logs_azka[sid]["logs"].append(log_data)

    shipment_logs_azka = list(shipment_logs_azka.values())
# ===================== POSISI KURIR TERKINI =====================
    cursor_azka.execute("""
        SELECT DISTINCT
            u.id_azka,
            u.username_azka,
            u.role_id_azka,
            r.nama_azka AS role_name_azka, 

            CASE 
                WHEN u.role_id_azka = 5 THEN 'DRIVER'
                WHEN u.role_id_azka = 3 THEN 'KURIR'
            END AS user_type,

            w.nama_azka AS warehouse_name_azka,
            w.address_azka,
            s.scan_type_azka,
            s.scan_time_azka,

            CASE
                WHEN s.scan_type_azka = 'OUT'
                    THEN 'DELIVERY'
                WHEN s.scan_type_azka = 'IN'
                    THEN 'WAREHOUSE'
                ELSE 'UNKNOWN'
            END AS delivery_status_azka

        FROM tbl_users_azka u

        -- ✅ JOIN ROLE
        LEFT JOIN tbl_roles_azka r
            ON u.role_id_azka = r.id_azka

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
    **totals_azka,
    shipment_logs_azka=shipment_logs_azka,
    total_couriers_azka=total_couriers_azka,
    total_driver_azka=total_driver_azka,
    courier_inside_azka=courier_inside_azka,
    courier_outside_azka=courier_outside_azka,
    courier_scan_logs_azka=courier_scan_logs_azka,
    courier_position_azka=courier_position_azka,
)
@app.route('/laporan_azka')
def laporan_azka():

    if 'user_id_azka' not in session:
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') != 1:
        return "Forbidden", 403

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # =============================
    # 1️⃣ STATUS SHIPMENT
    # =============================
    cursor.execute("""
        SELECT 
            status_azka,
            COUNT(*) AS total
        FROM tbl_shipment_azka
        GROUP BY status_azka
    """)
    shipment_status = cursor.fetchall()

    # =============================
    # 2️⃣ SHIPMENT PER GUDANG (TIDAK TERMASUK DELIVERED)
    # =============================
    cursor.execute("""
        SELECT 
            w.nama_azka,
            COUNT(s.id_azka) AS total
        FROM tbl_shipment_azka s
        JOIN tbl_warehouses_azka w 
            ON s.warehouse_id_azka = w.id_azka
        WHERE s.status_azka != 'DELIVERED'
        GROUP BY w.nama_azka
    """)
    shipment_per_warehouse = cursor.fetchall()

    # =============================
    # 3️⃣ AKTIVITAS KURIR (FIXED)
    # =============================
    cursor.execute("""
        SELECT 
            u.username_azka,
            COUNT(cs.id_azka) AS total_scan
        FROM tbl_users_azka u
        LEFT JOIN tbl_courier_scans_azka cs 
            ON u.id_azka = cs.courier_id_azka
        WHERE u.role_id_azka = 3
        GROUP BY u.username_azka
    """)
    courier_activity = cursor.fetchall()
    # =============================
    # 4️⃣ AKTIVITAS DRIVER
    # =============================
    cursor.execute("""
        SELECT 
            u.username_azka,
            COUNT(ds.id_azka) AS total_scan
        FROM tbl_users_azka u
        LEFT JOIN tbl_driver_scans_azka ds 
            ON u.id_azka = ds.driver_id_azka
        WHERE u.role_id_azka = 5
        GROUP BY u.username_azka
    """)
    driver_activity = cursor.fetchall()
    # =============================
    # 5️⃣ SHIPMENT PER KOTA TUJUAN
    # =============================
    cursor.execute("""
        SELECT 
            receiver_city_azka,
            COUNT(*) AS total
        FROM tbl_shipment_azka
        WHERE receiver_city_azka IS NOT NULL 
        AND receiver_city_azka != ''
        GROUP BY receiver_city_azka
    """)
    shipment_per_city = cursor.fetchall()
    # =============================
    # 6️⃣ TREN DELIVERED PER BULAN
    # =============================
    cursor.execute("""
        SELECT 
            DATE_FORMAT(updated_at_azka, '%Y-%m') AS bulan,
            COUNT(*) AS total
        FROM tbl_shipment_azka
        WHERE status_azka = 'DELIVERED'
        GROUP BY DATE_FORMAT(updated_at_azka, '%Y-%m')
        ORDER BY bulan ASC
    """)
    delivered_trend = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        'laporan_azka.html',
        username_azka=session['username_azka'],
        shipment_status=shipment_status,
        shipment_per_warehouse=shipment_per_warehouse,
        courier_activity=courier_activity,
        driver_activity=driver_activity,
        shipment_per_city=shipment_per_city,   # tambahkan ini
        delivered_trend=delivered_trend
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
        wilayah_azka = request.form.get('wilayah_azka')

        password_hash_azka = generate_password_hash(
            password_hash_azka,
            method='pbkdf2:sha256',
            salt_length=16
        )

        # cek role
        cursor.execute("SELECT nama_azka FROM tbl_roles_azka WHERE id_azka=%s", (role_id_azka,))
        role = cursor.fetchone()

        if role and role['nama_azka'].lower() == 'kurir':
            wilayah = wilayah_azka
        else:
            wilayah = None

        cursor.execute("""
            INSERT INTO tbl_users_azka
            (username_azka, email_azka, password_hash_azka, role_id_azka, is_active_azka, wilayah_azka)
            VALUES (%s, %s, %s, %s, 1, %s)
        """, (
            username_azka,
            email_azka,
            password_hash_azka,
            role_id_azka,
            wilayah
        ))

        conn.commit()
        flash("User berhasil ditambahkan!", "success")

        return redirect(url_for('admin_users_azka'))

    return render_template(
        'admin_users_azka.html',
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

    try:
        # 🔥 HAPUS DATA TERKAIT DULU
        cursor.execute("DELETE FROM tbl_activity_logs_azka WHERE user_id_azka = %s", (id_azka,))
        # 🔥 TERAKHIR: HAPUS USER
        cursor.execute("DELETE FROM tbl_users_azka WHERE id_azka = %s", (id_azka,))

        conn.commit()
        flash("User dan semua data terkait berhasil dihapus!", "success")

    except Exception as e:
        conn.rollback()
        flash(f"Terjadi error: {e}", "danger")

    finally:
        cursor.close()
        conn.close()

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
    ship_page = request.args.get('ship_page', default=1, type=int)

    limit = 15

    sys_offset = (sys_page - 1) * limit
    act_offset = (act_page - 1) * limit
    ship_offset = (ship_page - 1) * limit

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # ================= SYSTEM LOGS =================
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


    # ================= ACTIVITY LOGS (NON SYSTEM) =================
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tbl_activity_logs_azka
        WHERE actions_azka NOT IN ('Login','Logout')
        AND actions_azka NOT LIKE '%Shipment%'
    """)
    act_total = cursor.fetchone()['total']
    act_pages = (act_total + limit - 1) // limit

    cursor.execute("""
        SELECT l.*, u.username_azka, r.nama_azka
        FROM tbl_activity_logs_azka l
        INNER JOIN tbl_users_azka u ON l.user_id_azka = u.id_azka
        INNER JOIN tbl_roles_azka r ON u.role_id_azka = r.id_azka
        WHERE l.actions_azka NOT IN ('Login','Logout')
        AND l.actions_azka NOT LIKE '%Shipment%'
        ORDER BY l.created_at_azka DESC
        LIMIT %s OFFSET %s
    """, (limit, act_offset))
    activity_logs = cursor.fetchall()


    # ================= SHIPMENT LOGS =================
    # ================= SHIPMENT LOGS =================
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tbl_activity_logs_azka
        WHERE shipment_id_azka IS NOT NULL
    """)
    ship_total = cursor.fetchone()['total']
    ship_pages = (ship_total + limit - 1) // limit

    cursor.execute("""
        SELECT 
            l.id_azka,
            l.actions_azka,
            l.reference_azka,
            l.created_at_azka,

            s.tracking_number_azka,
            s.status_azka,

            driver.username_azka AS driver_name,
            courier.username_azka AS courier_name

        FROM tbl_activity_logs_azka l

        LEFT JOIN tbl_shipment_azka s 
            ON l.shipment_id_azka = s.id_azka

        LEFT JOIN tbl_users_azka driver
            ON s.driver_id_azka = driver.id_azka

        LEFT JOIN tbl_users_azka courier
            ON s.courier_id_azka = courier.id_azka

        WHERE l.shipment_id_azka IS NOT NULL
        ORDER BY l.created_at_azka DESC
        LIMIT %s OFFSET %s
    """, (limit, ship_offset))

    shipment_logs = cursor.fetchall()
    conn.close()

    return render_template(
        "activity_logs_azka.html",
        username_azka=session['username_azka'],

        system_logs=system_logs,
        activity_logs=activity_logs,
        shipment_logs=shipment_logs,

        sys_page=sys_page,
        sys_pages=sys_pages,

        act_page=act_page,
        act_pages=act_pages,

        ship_page=ship_page,
        ship_pages=ship_pages
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
            b.id_azka,
            b.tracking_number_azka,
            b.sender_name_azka,
            b.receiver_name_azka,
            b.receiver_address_azka,
            b.qr_code_data_azka,
            a.nama_barang_azka,
            a.berat_azka,
            a.qty_azka
        FROM
            tbl_products_azka a
        INNER JOIN tbl_shipment_azka b 
            ON a.shipment_id_azka = b.id_azka
    """)
    product_azka = cursor.fetchall()


    conn.close()

    return render_template(
        "product_azka.html",
                username_azka=session['username_azka'],
        product_azka=product_azka,

    )


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

    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    nama_azka = request.form['nama_azka']
    address_azka = request.form['address_azka']

    # 🌍 Geocoding alamat gudang
    lat, lng, city = get_lat_lng_city_from_address(address_azka)

    if lat is None or lng is None:
        flash(
            "❌ Alamat gudang tidak ditemukan di peta. Gunakan alamat lebih lengkap.",
            "warning"
        )
        return redirect(url_for('gudang_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    try:
        conn.start_transaction()

        # INSERT GUDANG
        cursor.execute("""
            INSERT INTO tbl_warehouses_azka
            (nama_azka, address_azka, latitude_azka, longitude_azka, city_azka)
            VALUES (%s, %s, %s, %s, %s)
        """, (nama_azka, address_azka, lat, lng, city))

        id_azka = cursor.lastrowid
        qr_data_azka = f"GUDANG|{id_azka}"

        # UPDATE QR
        cursor.execute("""
            UPDATE tbl_warehouses_azka
            SET qr_code_data_azka = %s
            WHERE id_azka = %s
        """, (qr_data_azka, id_azka))

        conn.commit()

        insert_log_azka(
            session['user_id_azka'],
            "Tambah Gudang",
            f"Gudang {nama_azka} ditambahkan di kota {city}"
        )

        flash("Gudang berhasil ditambahkan + lokasi otomatis 📍", "success")

    except Exception as e:
        conn.rollback()
        flash("Terjadi kesalahan saat menambahkan gudang", "danger")
        print("ERROR:", e)

    finally:
        conn.close()

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
            s.driver_id_azka,
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
        # ===== LOG CREATED =====
        cursor.execute("""
            INSERT INTO tbl_activity_logs_azka
            (user_id_azka, actions_azka, created_at_azka)
            VALUES (%s, %s, NOW())
        """, (
            session['user_id_azka'],
            f"Shipment {shipment_id}|CREATED|Shipment dibuat"
        ))
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

    if session.get('role_id_azka') != 1:
        return "Forbidden", 403

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    try:
        conn.start_transaction()

        # 🔒 LOCK DATA
        cursor.execute("""
            SELECT status_azka, tracking_number_azka
            FROM tbl_shipment_azka
            WHERE id_azka = %s
            FOR UPDATE
        """, (shipment_id,))
        shipment = cursor.fetchone()

        if not shipment:
            raise Exception("Shipment tidak ditemukan ❌")

        forbidden_status = [
            'DRIVER_ASSIGNED',
            'PICKUP',
            'ARRIVED_AT_ORIGIN_HUB',
            'IN_TRANSIT',
            'SORTING',
            'OUT_FOR_DELIVERY',
            'ON_THE_WAY',
            'DELIVERED'
        ]

        if shipment['status_azka'] in forbidden_status:
            raise Exception("Shipment sudah diproses, tidak bisa dihapus ❌")

        # =============================
        # LOG DULU (SEBELUM DELETE)
        # =============================
        cursor.execute("""
            INSERT INTO tbl_activity_logs_azka
            (user_id_azka, shipment_id_azka, actions_azka, reference_azka, created_at_azka)
            VALUES (%s,%s,%s,%s,NOW())
        """, (
            session['user_id_azka'],
            shipment_id,
            "DELETE_SHIPMENT",
            shipment['tracking_number_azka']
        ))

        # =============================
        # HAPUS FILE QR
        # =============================
        qr_path = f"static/qr_paket/{shipment['tracking_number_azka']}.png"
        if os.path.exists(qr_path):
            os.remove(qr_path)

        # =============================
        # HAPUS SHIPMENT (CASCADE)
        # =============================
        cursor.execute("""
            DELETE FROM tbl_shipment_azka 
            WHERE id_azka=%s
        """, (shipment_id,))

        conn.commit()
        flash("Shipment berhasil dihapus 🗑️", "success")

    except Exception as e:
        conn.rollback()
        flash(str(e), "danger")

    finally:
        conn.close()

    return redirect(url_for('shipment_azka'))
@app.route('/admin_scan_driver_assignment_azka', methods=['POST'])
def admin_scan_driver_assignment_azka():

    if 'user_id_azka' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    if session.get('role_id_azka') != 1:
        return jsonify({"message": "Forbidden"}), 403

    shipment_id = request.form.get('shipment_id')
    driver_qr = request.form.get('driver_qr')

    if not shipment_id or not driver_qr:
        return jsonify({"message": "Data tidak lengkap"}), 400

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    try:

        # ================= PARSE QR =================
        if "SOPIR|" in driver_qr:
            driver_id = driver_qr.split("|")[1]
        else:
            driver_id = driver_qr.strip()

        # ================= CEK DRIVER =================
        cursor.execute("""
            SELECT id_azka, username_azka
            FROM tbl_users_azka
            WHERE id_azka = %s
            AND role_id_azka = 5
        """, (driver_id,))

        driver = cursor.fetchone()

        if not driver:
            return jsonify({"message": "Driver tidak ditemukan"}), 404


        # ================= CEK SHIPMENT =================
        cursor.execute("""
            SELECT tracking_number_azka
            FROM tbl_shipment_azka
            WHERE id_azka = %s
        """, (shipment_id,))

        shipment = cursor.fetchone()

        if not shipment:
            return jsonify({"message": "Shipment tidak ditemukan"}), 404


        tracking_number = shipment['tracking_number_azka']


        # ================= ASSIGN DRIVER =================
        cursor.execute("""
            UPDATE tbl_shipment_azka
            SET driver_id_azka = %s,
                status_azka = 'DRIVER_ASSIGNED'
            WHERE id_azka = %s
        """, (driver['id_azka'], shipment_id))


        # ================= LOG =================
        log_text = f"Paket {tracking_number} sudah ditugaskan kepada driver {driver['username_azka']}"

        cursor.execute("""
            INSERT INTO tbl_activity_logs_azka
            (user_id_azka, shipment_id_azka, actions_azka, created_at_azka)
            VALUES (%s,%s,%s,NOW())
        """, (
            session['user_id_azka'],
            shipment_id,
            log_text
        ))

        conn.commit()

        return jsonify({
            "message": f"Driver {driver['username_azka']} ditugaskan"
        })

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
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

@app.route('/scan_kurir_ready_delivery_azka', methods=['POST'])
def scan_kurir_ready_delivery_azka():

    data = request.get_json()

    qr_kurir = data.get('qr_kurir')
    qr_paket = data.get('qr_paket')

    if not qr_kurir or not qr_paket:
        return jsonify({
            "status": "danger",
            "message": "❌ QR kurir & paket wajib discan"
        })

    # ================= PARSE QR =================
    try:
        qr_paket = qr_paket.strip().replace("\ufeff", "")
        qr_kurir = qr_kurir.strip().replace("\ufeff", "")

        # Parse QR Paket
        p = [x.strip() for x in qr_paket.split("|")]
        if len(p) != 3 or p[0].upper() != "PAKET":
            raise ValueError("QR Paket tidak valid")

        shipment_id = int(p[1])
        tracking = p[2]

        # Parse QR Kurir
        k = [x.strip() for x in qr_kurir.split("|")]
        if len(k) < 2 or k[0].upper() != "KURIR":
            raise ValueError("QR Kurir tidak valid")

        courier_id = int(k[1])

    except Exception as e:
        print("ERROR PARSE:", str(e))
        return jsonify({
            "status": "danger",
            "message": "❌ Format QR tidak valid"
        })

    # ================= VALIDASI SESSION =================
    warehouse_id = session.get('warehouse_id_azka')
    user_id = session.get('user_id_azka')

    if not warehouse_id or not user_id:
        return jsonify({
            "status": "danger",
            "message": "❌ Session gudang tidak valid"
        })

    conn = get_db_connection_azka()
    conn.autocommit = False
    cursor = conn.cursor(dictionary=True)

    try:
        # ================= LOCK SHIPMENT =================
        cursor.execute("""
            SELECT id_azka, status_azka, courier_id_azka,
                   receiver_city_azka, tracking_number_azka
            FROM tbl_shipment_azka
            WHERE id_azka=%s
            FOR UPDATE
        """, (shipment_id,))

        shipment = cursor.fetchone()

        if not shipment:
            conn.rollback()
            return jsonify({
                "status": "danger",
                "message": "❌ Paket tidak ditemukan"
            })

        if shipment['tracking_number_azka'] != tracking:
            conn.rollback()
            return jsonify({
                "status": "danger",
                "message": "❌ Tracking tidak cocok"
            })


        if shipment['status_azka'] == 'READY_FOR_DELIVERY':
            conn.rollback()
            return jsonify({
                "status": "danger",
                "message": "❌ Paket sudah diambil kurir"
            })


        # ================= AMBIL DATA KURIR =================
        cursor.execute("""
            SELECT id_azka, username_azka, wilayah_azka
            FROM tbl_users_azka
            WHERE id_azka=%s AND role_id_azka=3
        """, (courier_id,))

        courier = cursor.fetchone()

        if not courier:
            conn.rollback()
            return jsonify({
                "status": "danger",
                "message": "❌ Kurir tidak ditemukan"
            })

        # ================= VALIDASI WILAYAH =================
        if not shipment['receiver_city_azka'] or not courier['wilayah_azka']:
            conn.rollback()
            return jsonify({
                "status": "danger",
                "message": "❌ Wilayah belum diset pada paket / kurir"
            })

        city = shipment['receiver_city_azka'].strip().upper()
        wilayah = courier['wilayah_azka'].strip().upper()

        if city != wilayah:
            conn.rollback()
            return jsonify({
                "status": "danger",
                "message": "❌ Paket bukan wilayah kurir ini"
            })
        # ================= UPDATE SHIPMENT =================
        cursor.execute("""
            UPDATE tbl_shipment_azka
            SET
                status_azka='READY_FOR_DELIVERY',
                courier_id_azka=%s
            WHERE id_azka=%s
        """, (courier_id, shipment_id))

        # ================= ACTIVITY LOG =================
        cursor.execute("""
            INSERT INTO tbl_activity_logs_azka
            (user_id_azka, shipment_id_azka, actions_azka, reference_azka)
            VALUES (%s,%s,%s,%s)
        """, (
            user_id,
            shipment_id,
            f"🚚 Paket {tracking} diserahkan ke kurir {courier['username_azka']}",
            tracking
        ))

        conn.commit()

        return jsonify({
            "status": "success",
            "message": f"✅ Paket berhasil diserahkan ke {courier['username_azka']}"
        })

    except Exception as e:
        conn.rollback()
        print("ERROR DETAIL:", str(e))
        return jsonify({
            "status": "danger",
            "message": "❌ Terjadi kesalahan sistem"
        })

    finally:
        conn.close()
@app.route('/scan_sortir_azka', methods=['POST'])
def scan_sortir_azka():

    if 'user_id_azka' not in session:
        return jsonify({"status": "danger", "message": "Unauthorized"}), 401

    data = request.get_json()
    raw_qr = data.get('qr_paket')  # samakan dengan frontend

    if not raw_qr:
        return jsonify({
            "status": "danger",
            "message": "❌ QR kosong"
        })

    try:
        raw_qr = raw_qr.strip().replace("\n", "").replace("\r", "").replace("\ufeff", "")

        parts = [x.strip() for x in raw_qr.split("|")]

        if len(parts) != 3 or parts[0].upper() != "PAKET":
            raise ValueError("QR Paket tidak valid")

        shipment_id = int(parts[1])
        tracking = parts[2]

    except Exception as e:
        print("ERROR PARSE:", raw_qr)
        print("DETAIL:", str(e))
        return jsonify({
            "status": "danger",
            "message": "❌ Format QR tidak valid"
        })

    conn = get_db_connection_azka()
    conn.autocommit = False
    cursor = conn.cursor(dictionary=True)

    # Lock data
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

    if shipment['status_azka'] == 'SORTING':
        conn.close()
        return jsonify({
            "status": "warning",
            "message": "⚠️ Paket sudah disortir"
        })

    if shipment['status_azka'] != 'TRANSIT_HUB':
        conn.close()
        return jsonify({
            "status": "danger",
            "message": "❌ Paket belum masuk gudang"
        })

    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka='SORTING'
        WHERE id_azka=%s
    """, (shipment_id,))

    cursor.execute("""
        INSERT INTO tbl_activity_logs_azka
        (user_id_azka, actions_azka, created_at_azka)
        VALUES (%s,%s,NOW())
    """, (
        session.get('user_id_azka'),
        f"📦 Paket  masuk sortir | {tracking}"
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": f"✅ Paket {tracking} masuk sortir",
        "reload": False
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



@app.route('/kurir_dashboard_azka')
def kurir_dashboard_azka():
    # ================= CEK LOGIN =================
    if 'user_id_azka' not in session:
        return redirect(url_for('login_azka'))

    # ================= CEK ROLE KURIR (3) =================
    if session.get('role_id_azka') != 3:
        flash("Akses ditolak", "danger")
        return redirect(url_for('dashboard_azka'))

    conn_azka = get_db_connection_azka()
    cursor_azka = conn_azka.cursor(dictionary=True)

    try:
        user_id = session['user_id_azka']

        # ================= DATA KURIR =================
        cursor_azka.execute("""
            SELECT id_azka, username_azka
            FROM tbl_users_azka
            WHERE id_azka = %s
        """, (user_id,))
        kurir_azka = cursor_azka.fetchone()

        # Jika user tidak ditemukan
        if not kurir_azka:
            flash("Data kurir tidak ditemukan.", "danger")
            return redirect(url_for('login_azka'))

        # ================= SCAN TERAKHIR =================
        cursor_azka.execute("""
            SELECT cs.*, w.nama_azka
            FROM tbl_courier_scans_azka cs
            LEFT JOIN tbl_warehouses_azka w 
                ON cs.warehouse_id_azka = w.id_azka
            WHERE cs.courier_id_azka = %s
            ORDER BY cs.scan_time_azka DESC
            LIMIT 1
        """, (user_id,))
        last_scan_azka = cursor_azka.fetchone()

    finally:
        cursor_azka.close()
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
        return jsonify({"message": "Unauthorized"}), 401

    if session.get('role_id_azka') != 3:
        return jsonify({"message": "Forbidden"}), 403

    courier_id = session['user_id_azka']
    scan_type = request.form.get('scan_type_azka')
    warehouse_id = request.form.get('warehouse_id_azka')
    package_code = request.form.get('package_code')

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    try:
        conn.start_transaction()

        # =====================================================
        # ===================== OUT ===========================
        # =====================================================
        if scan_type == "OUT":

            if not warehouse_id:
                return jsonify({"message": "Scan gudang wajib"}), 400

            warehouse_id = int(warehouse_id)

            # Validasi gudang
            cursor.execute("""
                SELECT id_azka FROM tbl_warehouses_azka
                WHERE id_azka=%s
            """, (warehouse_id,))
            if not cursor.fetchone():
                conn.rollback()
                return jsonify({"message": "Gudang tidak valid"}), 400

            # Tidak boleh masih ON_THE_WAY
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM tbl_shipment_azka
                WHERE courier_id_azka=%s
                AND status_azka='ON_THE_WAY'
            """, (courier_id,))
            if cursor.fetchone()['total'] > 0:
                conn.rollback()
                return jsonify({
                    "message": "Masih ada paket belum terkirim"
                }), 400

            # Ambil paket sesuai gudang
            cursor.execute("""
                SELECT 
                    s.id_azka,
                    s.tracking_number_azka,
                    s.receiver_name_azka,
                    s.receiver_city_azka,
                    p.nama_barang_azka AS product_name_azka,
                    p.berat_azka AS weight_azka
                FROM tbl_shipment_azka s
                LEFT JOIN tbl_products_azka p
                    ON p.shipment_id_azka = s.id_azka
                WHERE s.courier_id_azka=%s
                AND s.status_azka='READY_FOR_DELIVERY'
                AND s.warehouse_id_azka=%s
                ORDER BY s.created_at_azka ASC
                LIMIT 10
                FOR UPDATE
            """, (courier_id, warehouse_id))

            shipments = cursor.fetchall()

            if not shipments:
                conn.rollback()
                return jsonify({
                    "message": "Tidak ada paket di gudang ini"
                }), 400

            shipment_ids = [s['id_azka'] for s in shipments]

            # Update status
            cursor.execute(f"""
                UPDATE tbl_shipment_azka
                SET status_azka='ON_THE_WAY'
                WHERE id_azka IN ({','.join(['%s']*len(shipment_ids))})
            """, shipment_ids)

            # Insert scan + log
            for shipment in shipments:

                cursor.execute("""
                    INSERT INTO tbl_courier_scans_azka
                    (courier_id_azka, shipment_id_azka, warehouse_id_azka, scan_type_azka, scan_time_azka)
                    VALUES (%s,%s,%s,'OUT',NOW())
                """, (courier_id, shipment['id_azka'], warehouse_id))

                cursor.execute("""
                    INSERT INTO tbl_activity_logs_azka
                    (user_id_azka, shipment_id_azka, actions_azka, reference_azka)
                    VALUES (%s,%s,%s,%s)
                """, (
                    courier_id,
                    shipment['id_azka'],
                    f"Paket {shipment['tracking_number_azka']} sedang dalam pengantaran",
                    shipment['tracking_number_azka']
                ))

            conn.commit()

            return jsonify({
                "message": "Paket berhasil diambil",
                "data": shipments
            }), 200

        # =====================================================
        # ================= DELIVERED =========================
        # =====================================================
        elif scan_type == "PACKAGE":

            if not package_code:
                return jsonify({"message": "QR paket tidak valid"}), 400

            shipment_id = int(package_code)

            cursor.execute("""
                SELECT *
                FROM tbl_shipment_azka
                WHERE id_azka=%s
                FOR UPDATE
            """, (shipment_id,))

            shipment = cursor.fetchone()

            if not shipment:
                return jsonify({"message": "Paket tidak ditemukan"}), 404

            if shipment['courier_id_azka'] != courier_id:
                return jsonify({"message": "Bukan milik kurir ini"}), 403

            if shipment['status_azka'] != 'ON_THE_WAY':
                return jsonify({
                    "message": f"Status paket masih {shipment['status_azka']}"
                }), 400

            # Update status
            cursor.execute("""
                UPDATE tbl_shipment_azka
                SET status_azka='DELIVERED',
                    courier_id_azka=NULL
                WHERE id_azka=%s
            """, (shipment_id,))

            # Insert scan
            cursor.execute("""
                INSERT INTO tbl_courier_scans_azka
                (courier_id_azka, shipment_id_azka, scan_type_azka, scan_time_azka)
                VALUES (%s,%s,'DELIVERED',NOW())
            """, (courier_id, shipment_id))

            # Activity log
            cursor.execute("""
                INSERT INTO tbl_activity_logs_azka
                (user_id_azka, shipment_id_azka, actions_azka, reference_azka)
                VALUES (%s,%s,%s,%s)
            """, (
                courier_id,
                shipment_id,
                f"Paket {shipment['tracking_number_azka']} sudah diterima oleh {shipment['receiver_name_azka']}",
                shipment['tracking_number_azka']
            ))

            conn.commit()
            return jsonify({"message": "Paket berhasil diserahkan"}), 200

        # =====================================================
        # ================= RETURN ============================
        # =====================================================
        elif scan_type == "RETURN":

            if not warehouse_id:
                return jsonify({"message": "Scan gudang wajib"}), 400

            warehouse_id = int(warehouse_id)

            # ================= LOCK KURIR =================
            cursor.execute("""
                SELECT id_azka
                FROM tbl_users_azka
                WHERE id_azka=%s
                FOR UPDATE
            """, (courier_id,))

            if not cursor.fetchone():
                conn.rollback()
                return jsonify({
                    "message": "Kurir tidak valid"
                }), 400

            # ================= VALIDASI GUDANG =================
            cursor.execute("""
                SELECT id_azka
                FROM tbl_warehouses_azka
                WHERE id_azka=%s
                FOR UPDATE
            """, (warehouse_id,))

            if not cursor.fetchone():
                conn.rollback()
                return jsonify({
                    "message": "Gudang tidak valid"
                }), 400

            # ================= CEK SUDAH OUT ATAU BELUM =================
            cursor.execute("""
                SELECT warehouse_id_azka
                FROM tbl_courier_scans_azka
                WHERE courier_id_azka=%s
                AND scan_type_azka='OUT'
                ORDER BY scan_time_azka DESC
                LIMIT 1
                FOR UPDATE
            """, (courier_id,))

            last_out = cursor.fetchone()

            if not last_out:
                conn.rollback()
                return jsonify({
                    "message": "Kurir belum mengambil paket"
                }), 400

            # Pastikan return ke gudang yang sama
            if last_out['warehouse_id_azka'] != warehouse_id:
                conn.rollback()
                return jsonify({
                    "message": "Harus kembali ke gudang asal"
                }), 400

            # ================= LOCK SEMUA PAKET AKTIF =================
            cursor.execute("""
                SELECT 
                    id_azka,
                    tracking_number_azka,
                    status_azka
                FROM tbl_shipment_azka
                WHERE courier_id_azka=%s
                AND status_azka IN (
                    'READY_FOR_DELIVERY',
                    'ON_THE_WAY',
                    'FAILED_DELIVERY',
                    'RETURN_TO_SENDER'
                )
                FOR UPDATE
            """, (courier_id,))

            active_shipments = cursor.fetchall()

            if active_shipments:
                paket_list = ", ".join(
                    [p['tracking_number_azka'] for p in active_shipments]
                )

                conn.rollback()
                return jsonify({
                    "message": f"Masih membawa paket: {paket_list}"
                }), 400

            # ================= CEK ADA PAKET NYANGKUT =================
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM tbl_shipment_azka
                WHERE courier_id_azka=%s
                AND status_azka NOT IN (
                    'DELIVERED',
                    'CANCELLED'
                )
                FOR UPDATE
            """, (courier_id,))

            sisa = cursor.fetchone()['total']

            if sisa > 0:
                conn.rollback()
                return jsonify({
                    "message": "Masih ada paket belum selesai"
                }), 400

            # ================= INSERT RETURN =================
            cursor.execute("""
                INSERT INTO tbl_courier_scans_azka
                (
                    courier_id_azka,
                    warehouse_id_azka,
                    scan_type_azka,
                    scan_time_azka
                )
                VALUES (%s,%s,'RETURN',NOW())
            """, (courier_id, warehouse_id))

            # ================= ACTIVITY LOG =================
            cursor.execute("""
                INSERT INTO tbl_activity_logs_azka
                (
                    user_id_azka,
                    shipment_id_azka,
                    actions_azka,
                    created_at_azka
                )
                VALUES (%s,NULL,%s,NOW())
            """, (
                courier_id,
                "Kurir kembali ke gudang"
            ))

            conn.commit()

            return jsonify({
                "message": "Kurir berhasil kembali ke gudang"
            }), 200
    except Exception as e:
        conn.rollback()
        print("SCAN ERROR:", e)
        return jsonify({"message": "Terjadi kesalahan server"}), 500

    finally:
        cursor.close()
        conn.close()
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

    # =============================
    # AUTH
    # =============================
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
    cursor = conn.cursor(dictionary=True)

    try:
        conn.start_transaction()

        # =============================
        # CEK PENUGASAN ADMIN
        # =============================
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM tbl_shipment_azka
            WHERE driver_id_azka=%s
            AND status_azka IN (
                'DRIVER_ASSIGNED',
                'PICKUP',
                'ARRIVED_AT_ORIGIN_HUB',
                'IN_TRANSIT'
            )
        """, (driver_id,))

        assigned = cursor.fetchone()['total']

        if assigned == 0:
            raise Exception("Belum ada shipment ditugaskan oleh admin")

        # =============================
        # VALIDASI POLA SCAN (IN → OUT → IN)
        # =============================
        cursor.execute("""
            SELECT scan_type_azka, warehouse_id_azka
            FROM tbl_driver_scans_azka
            WHERE driver_id_azka=%s
            ORDER BY scan_time_azka DESC
            LIMIT 1
            FOR UPDATE
        """, (driver_id,))

        last_scan = cursor.fetchone()

        if last_scan:
            if last_scan['scan_type_azka'] == 'IN' and scan_type != 'OUT':
                raise Exception("Setelah IN wajib OUT dulu")

            if last_scan['scan_type_azka'] == 'OUT' and scan_type != 'IN':
                raise Exception("Setelah OUT wajib IN dulu")
        else:
            if scan_type != 'IN':
                raise Exception("Scan pertama wajib IN")

        # =============================
        # VALIDASI GUDANG
        # =============================
        cursor.execute("""
            SELECT id_azka, nama_azka, latitude_azka, longitude_azka
            FROM tbl_warehouses_azka
            WHERE id_azka=%s
        """, (warehouse_id,))

        wh = cursor.fetchone()

        if not wh:
            raise Exception("Gudang tidak ditemukan")

        # =============================
        # AMBIL SHIPMENT DRIVER (LOCK)
        # =============================
        cursor.execute("""
            SELECT id_azka,
                   status_azka,
                   tracking_number_azka,
                   is_interisland,
                   warehouse_id_azka
            FROM tbl_shipment_azka
            WHERE driver_id_azka=%s
            AND status_azka NOT IN (
                'DELIVERED',
                'READY_FOR_DELIVERY',
                'TRANSIT_HUB'
            )
            FOR UPDATE
        """, (driver_id,))

        shipments = cursor.fetchall()

        if not shipments:
            raise Exception("Tidak ada shipment aktif")

        updated_count = 0

        # =============================
        # FLOW STATUS
        # =============================
        next_status_map = {
            'DRIVER_ASSIGNED': 'PICKUP',
            'PICKUP': 'ARRIVED_AT_ORIGIN_HUB',
            'ARRIVED_AT_ORIGIN_HUB': 'IN_TRANSIT',
            'IN_TRANSIT': 'TRANSIT_HUB',
        }

        for s in shipments:

            current_status = s['status_azka']
            next_status = next_status_map.get(current_status)

            if not next_status:
                continue

            # =============================
            # VALIDASI ORIGIN (SUPER PENTING)
            # =============================
            if current_status == 'DRIVER_ASSIGNED':

                if scan_type != 'IN':
                    raise Exception("Scan pertama di gudang asal wajib IN")

                if s['warehouse_id_azka'] != warehouse_id:
                    raise Exception(
                        f"Shipment {s['tracking_number_azka']} bukan dari gudang ini"
                    )

            new_driver = driver_id

            # Driver dilepas saat sampai TRANSIT
            if next_status == 'TRANSIT_HUB':
                new_driver = None

            # =============================
            # UPDATE SHIPMENT
            # =============================
            cursor.execute("""
                UPDATE tbl_shipment_azka
                SET status_azka=%s,
                    warehouse_id_azka=%s,
                    driver_id_azka=%s
                WHERE id_azka=%s
            """, (
                next_status,
                warehouse_id,
                new_driver,
                s['id_azka']
            ))

            # =============================
            # INSERT LOG
            # =============================
            desc = get_description(
                next_status,
                wh['nama_azka'],
                s['is_interisland']
            )

            cursor.execute("""
                INSERT INTO tbl_activity_logs_azka
                (user_id_azka, actions_azka, created_at_azka)
                VALUES (%s,%s,NOW())
            """, (
                driver_id,
                f"{desc} | {s['tracking_number_azka']}"
            ))

            updated_count += 1

        # =============================
        # INSERT DRIVER SCAN
        # =============================
        cursor.execute("""
            INSERT INTO tbl_driver_scans_azka
            (driver_id_azka,
             warehouse_id_azka,
             scan_type_azka,
             latitude_azka,
             longitude_azka,
             scan_time_azka)
            VALUES (%s,%s,%s,%s,%s,NOW())
        """, (
            driver_id,
            warehouse_id,
            scan_type,
            wh['latitude_azka'],
            wh['longitude_azka']
        ))

        conn.commit()

        return f"OK - {updated_count} shipment diproses"

    except Exception as e:
        conn.rollback()
        return str(e), 400

    finally:
        conn.close()
@app.route('/dashboard_sopir_azka')
def dashboard_sopir_azka():
    if 'user_id_azka' not in session:
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') != 5:
        flash("Akses ditolak", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # 👤 Data kurir
    cursor.execute("""
        SELECT id_azka, username_azka
        FROM tbl_users_azka
        WHERE id_azka = %s
    """, (session['user_id_azka'],))
    kurir_azka = cursor.fetchone()

    # 🔄 Scan terakhir
    cursor.execute("""
        SELECT cs.*, w.nama_azka
        FROM tbl_driver_scans_azka cs
        LEFT JOIN tbl_warehouses_azka w 
            ON cs.warehouse_id_azka = w.id_azka
        WHERE cs.driver_id_azka = %s
        ORDER BY cs.scan_time_azka DESC
        LIMIT 1
    """, (session['user_id_azka'],))
    last_scan_azka = cursor.fetchone()

    cursor.execute("""
        SELECT 
            a.created_at_azka,
            a.actions_azka,
            b.username_azka
        FROM tbl_activity_logs_azka a
        INNER JOIN tbl_users_azka b 
            ON a.user_id_azka = b.id_azka
        WHERE a.user_id_azka = %s
        AND a.actions_azka LIKE '%%|%%'
        ORDER BY a.created_at_azka DESC
        LIMIT 50
    """, (session['user_id_azka'],))
    riwayat_pengiriman = cursor.fetchall()




    cursor.execute("""
        SELECT COUNT(*) as total
        FROM tbl_shipment_azka
        WHERE driver_id_azka = %s
        AND status_azka NOT IN ('DELIVERED','READY_FOR_DELIVERY')
    """, (session['user_id_azka'],))
    shipment_active = cursor.fetchone()['total']
    conn.close()
    return render_template(
        'dashboard_sopir_azka.html',
        kurir_azka=kurir_azka,
        last_scan_azka=last_scan_azka,
        riwayat_pengiriman=riwayat_pengiriman,
        shipment_active=shipment_active
    )


@app.route('/logout_azka')
def logout_azka():

    # 📝 CATAT LOG SEBELUM SESSION DIHAPUS
    if session.get('logged_in_azka'):
        insert_log_azka(
            session.get('user_id_azka'),
            "Logout",
            f"User {session.get('username_azka')} berhasil logout"
        )

    # 🔐 HAPUS SEMUA SESSION
    session.clear()

    flash("Berhasil logout!", "success")
    return redirect(url_for('login_azka'))

if __name__ == "__main__":
    app.run(debug=True)
