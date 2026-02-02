from flask import Flask, render_template, request, redirect, session, flash, url_for,current_app
from werkzeug.security import generate_password_hash, check_password_hash
from io import BytesIO
from flask import send_file
import mysql.connector
import qrcode
import os
import time
import requests
import re

app = Flask(__name__)
app.secret_key = 'Azka123'


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

def get_lat_lng_from_address(address):
    try:
        time.sleep(1)
        url = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "LogisticsAzka/1.0"}

        queries = [
            address,
            "Cibeureum Cimahi Selatan",
            "Cimahi Selatan",
            "Cimahi"
        ]

        for q in queries:
            res = requests.get(url, params={
                "q": q,
                "format": "json",
                "limit": 1
            }, headers=headers, timeout=10)

            data = res.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])

    except Exception as e:
        print("Geocoding error:", e)

    return None, None

def normalize_address(address):
    address = address.lower()
    address = address.replace("no.", "")
    address = address.replace("jl.", "jalan")
    address = address.replace("kec.", "")
    address = address.replace("kab.", "")
    address = address.replace("kota", "")
    return address.strip()

def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name.lower())

def count_shipment_status(cursor, status):
    cursor.execute("""
        SELECT COUNT(*) 
        FROM tbl_shipment_azka
        WHERE status_pengiriman_azka = %s
    """, (status,))
    return cursor.fetchone()[0]

@app.route('/', methods=['GET', 'POST'])
@app.route('/login_azka', methods=['GET', 'POST'])
def login_azka():
    if request.method == "POST":
        username_azka = request.form['username_azka']
        password_azka = request.form['password_azka']

        conn = get_db_connection_azka()
        cursor = conn.cursor(dictionary=True)

        query_azka = "SELECT * FROM tbl_users_azka WHERE username_azka = %s"
        cursor.execute(query_azka, (username_azka,))
        user_azka = cursor.fetchone()

        cursor.close()
        conn.close()

        # Username tidak ditemukan
        if not user_azka:
            flash("Username tidak ditemukan!", "danger")
            return redirect(url_for('login_azka'))

        # Cek password hash
        if check_password_hash(user_azka['password_hash_azka'], password_azka):
            session['user_id_azka'] = user_azka['id_azka']
            session['username_azka'] = user_azka['username_azka']
            session['role_id_azka'] = user_azka['role_id_azka']

            insert_log_azka(
                user_azka['id_azka'],
                "Login",
                f"User {user_azka['username_azka']} berhasil login"
            )


            flash("Login berhasil!", "success")
            return redirect(url_for('dashboard_azka'))
        else:
            flash("Password salah!", "danger")
            return redirect(url_for('login_azka'))

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
        4: 'manager_dashboard_azka'
    }

    if role_azka in dashboard_map_azka:
        return redirect(url_for(dashboard_map_azka[role_azka]))

    flash("Role tidak dikenali!", "danger")
    return redirect(url_for('login_azka'))


# ===========================
#   ADMIN DASHBOARD
# ===========================
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

    # ===================== LIST TAHUN =====================
    #cursor_azka.execute("""
        #SELECT DISTINCT YEAR(created_at_azka) AS tahun_azka
        #FROM tbl_shipment_azka
        #ORDER BY tahun_azka DESC
    #""")
    #list_tahun_azka = [row['tahun_azka'] for row in cursor_azka.fetchall()]

    #if not tahun_azka and list_tahun_azka:
        #tahun_azka = list_tahun_azka[0]
    #tahun_azka = int(tahun_azka)

    # ===================== TOTAL DATA =====================
    tables_azka = {
        "total_users_azka": "tbl_users_azka",
        "total_warehouses_azka": "tbl_warehouses_azka",
        "total_shipment_azka": "tbl_shipment_azka",
        "total_receiving_azka": "tbl_receiving_azka",
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
        'created',
        'received',
        'sorted',
        'in_transit',
        'arrived_hub',
        'out_for_delivery',
        'delivered',
        'failed'
    ]

    status_count_azka = {}
    for status_azka in status_list_azka:
        cursor_azka.execute("""
            SELECT COUNT(*) AS total_azka
            FROM tbl_shipment_azka
            WHERE status_azka = %s
        """, (status_azka,))
        status_count_azka[status_azka] = cursor_azka.fetchone()['total_azka']

    # ===================== STATUS TERAKHIR =====================
    #cursor_azka.execute("""
        #SELECT status_azka
        #FROM tbl_shipment_azka
        #ORDER BY updated_at_azka DESC
        #LIMIT 1
    #""")
    #row_azka = cursor_azka.fetchone()
    #current_status_azka = row_azka['status_azka'] if row_azka else None

    # ===================== DATA BULANAN =====================
    #def data_bulanan_azka(table_azka):
        #cursor_azka.execute(f"""
            #SELECT MONTH(created_at_azka) AS bulan_azka, COUNT(*) AS total_azka
            #FROM {table_azka}
            #WHERE YEAR(created_at_azka) = %s
            #GROUP BY bulan_azka
            #ORDER BY bulan_azka
        #""", (tahun_azka,))
        #return cursor_azka.fetchall()

    #barang_masuk_raw_azka  = data_bulanan_azka("tbl_receiving_azka")
    #barang_keluar_raw_azka = data_bulanan_azka("tbl_shipment_azka")

    #def map_bulan_azka(data_azka):
        #hasil_azka = [0] * 12
        #for row_azka in data_azka:
            #hasil_azka[row_azka['bulan_azka'] - 1] = row_azka['total_azka']
        #return hasil_azka

    # ===================== LOG SCAN KURIR =====================
    cursor_azka.execute("""
        SELECT u.username_azka AS courier_name_azka,
            l.actions_azka,
            l.created_at_azka
        FROM tbl_activity_logs_azka l
        JOIN tbl_users_azka u ON l.user_id_azka = u.id_azka
        WHERE u.role_id_azka = 3
        ORDER BY l.created_at_azka DESC
        LIMIT 10
    """)
    courier_logs_azka = cursor_azka.fetchall()

    # ===================== POSISI KURIR TERKINI =====================
    cursor_azka.execute("""
        SELECT 
            u.id_azka,
            u.username_azka,
            w.nama_azka AS warehouse_name_azka,
            w.address_azka,
            s.scan_type_azka,
            s.scan_time_azka
        FROM tbl_users_azka u
        LEFT JOIN (
            SELECT cs.*
            FROM tbl_courier_scans_azka cs
            JOIN (
                SELECT 
                    courier_id_azka, 
                    MAX(scan_time_azka) AS last_scan
                FROM tbl_courier_scans_azka
                GROUP BY courier_id_azka
            ) last_scan
            ON cs.courier_id_azka = last_scan.courier_id_azka
            AND cs.scan_time_azka = last_scan.last_scan
        ) s ON u.id_azka = s.courier_id_azka
        LEFT JOIN tbl_warehouses_azka w 
            ON s.warehouse_id_azka = w.id_azka
        WHERE u.role_id_azka = 3
        ORDER BY u.username_azka;

    """)

    courier_position_azka = cursor_azka.fetchall()

    # ===================== LOG SCAN KURIR (MONITORING) =====================
    cursor_azka.execute("""
        SELECT 
            u.username_azka AS courier_name_azka,
            cs.scan_type_azka,
            w.nama_azka AS warehouse_name_azka,
            cs.scan_time_azka
        FROM tbl_courier_scans_azka cs
        JOIN tbl_users_azka u ON cs.courier_id_azka = u.id_azka
        LEFT JOIN tbl_warehouses_azka w ON cs.warehouse_id_azka = w.id_azka
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
        FROM tbl_product_azka l
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

@app.route('/product_add_azka', methods=['POST'])
def product_add_azka():
    sku_azka = request.form['sku_azka']
    nama_product_azka = request.form['nama_product_azka']
    category_id_azka = request.form['category_id_azka']
    unit_azka = request.form['unit_azka']
    min_stock_azka = request.form['min_stock_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_product_azka 
        (sku_azka, nama_product_azka, category_id_azka, unit_azka, min_stock_azka)
        VALUES (%s, %s, %s, %s, %s)
    """, (sku_azka, nama_product_azka, category_id_azka, unit_azka, min_stock_azka))

    conn.commit()
    conn.close()

    insert_log_azka(session['user_id_azka'], "Tambah Data", f"Barang #{sku_azka} di tambahkan")
    flash("Berhasil menambah data barang!", "success")
    return redirect(url_for('product_azka'))

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
            UPDATE tbl_product_azka SET
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

    cursor.execute("SELECT * FROM tbl_product_azka WHERE id_azka=%s", (id_azka,))
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

    cursor.execute("SELECT nama_azka FROM tbl_product_azka WHERE id_azka=%s", (id_azka,))
    row = cursor.fetchone()
    nama_barang = row[0] if row else "Tidak diketahui"

    cursor.execute("DELETE FROM tbl_product_azka WHERE id_azka=%s", (id_azka,))
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


@app.route('/receiving_azka')
def receiving_azka():
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
        a.id_azka,
        a.product_id_azka,
        b.nama_product_azka,
        a.batch_number_azka,
        a.quantity_received_azka,
        a.quantity_accepted_azka,
        a.expire_date_azka
    FROM
        tbl_receiving_items_azka a
    INNER JOIN tbl_product_azka b ON
        a.product_id_azka = b.id_azka
    ORDER BY a.id_azka ASC;
    """)

    receiving_azka = cursor.fetchall()
    
    cursor.execute("SELECT id_azka, nama_product_azka FROM tbl_product_azka ")
    product_list = cursor.fetchall()

    cursor.execute("SELECT id_azka, status_azka FROM tbl_receiving_azka ")
    status_azka = cursor.fetchall()

    cursor.execute("""
    SELECT
        a.id_azka,
        a.po_id_azka,
        a.warehouse_id_azka,
        a.received_by_azka,
        a.status_azka,

        b.nama_azka AS warehouse_name,
        c.po_number_azka,
        d.username_azka
    FROM tbl_receiving_azka a
    LEFT JOIN tbl_warehouses_azka b ON a.warehouse_id_azka = b.id_azka
    LEFT JOIN tbl_purchase_orders_azka c ON a.po_id_azka = c.id_azka
    LEFT JOIN tbl_users_azka d ON a.received_by_azka = d.id_azka;
    """)
    rece_azka = cursor.fetchall()

    cursor.execute("SELECT id_azka, po_number_azka FROM tbl_purchase_orders_azka")
    dropdown_po = cursor.fetchall()

    cursor.execute("SELECT id_azka, nama_azka FROM tbl_warehouses_azka")
    dropdown_gudang = cursor.fetchall()

    cursor.execute("SELECT id_azka, username_azka FROM tbl_users_azka")
    dropdown_users_azka = cursor.fetchall()


    conn.close()

    return render_template(
    "receiving_azka.html",
    username_azka=session['username_azka'],
    receiving_azka=receiving_azka,
    product_list=product_list,
    rece_azka=rece_azka,
    status_azka=status_azka,
    dropdown_po=dropdown_po,
    dropdown_gudang=dropdown_gudang,
    dropdown_users_azka=dropdown_users_azka
)

    
@app.route('/receiving_add_azka', methods=['POST'])
def receiving_add_azka():
    receiving_id_azka = request.form['receiving_id_azka']
    product_id_azka = request.form['product_id_azka']
    batch_number_azka = request.form['batch_number_azka']
    quantity_received_azka = request.form['quantity_received_azka']
    quantity_accepted_azka = request.form['quantity_accepted_azka']
    expire_date_azka = request.form['expire_date_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_receiving_items_azka 
        (receiving_id_azka, product_id_azka, batch_number_azka, quantity_received_azka,quantity_accepted_azka,expire_date_azka)
        VALUES (%s, %s, %s, %s,%s,%s)
    """, (receiving_id_azka, product_id_azka, batch_number_azka, quantity_received_azka,quantity_accepted_azka,expire_date_azka))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Data barang masuk berhasil ditambahkan!", "success")
    return redirect('/receiving_azka')

@app.route('/receiving_edit_azka/<int:id_azka>', methods=['GET', 'POST'])
def receiving_edit_azka(id_azka):
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in [1, 2]:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        product_id_azka = request.form['product_id_azka']
        batch_number_azka = request.form['batch_number_azka']
        quantity_received_azka = request.form['quantity_received_azka']
        quantity_accepted_azka = request.form['quantity_accepted_azka']
        expire_date_azka = request.form['expire_date_azka']

        cursor.execute("""
            UPDATE tbl_receiving_items_azka SET
                product_id_azka = %s,
                batch_number_azka = %s,
                quantity_received_azka = %s,
                quantity_accepted_azka = %s,
                expire_date_azka = %s
            WHERE id_azka = %s
        """, (product_id_azka, batch_number_azka, quantity_received_azka,
              quantity_accepted_azka, expire_date_azka, id_azka))
        conn.commit()

        conn.close()

        insert_log_azka(session['user_id_azka'], "Edit Receiving",
                        f"Receiving ID {id_azka} diperbarui")

        flash("Data receiving berhasil diperbarui!", "success")
        return redirect(url_for('receiving_azka'))

    cursor.execute("""
        SELECT 
            r.*, p.nama_product_azka
        FROM tbl_receiving_items_azka r
        INNER JOIN tbl_product_azka p 
            ON r.product_id_azka = p.id_azka
        WHERE r.id_azka = %s
    """, (id_azka,))
    receiving_azka = cursor.fetchone()


    cursor.execute("SELECT id_azka, nama_product_azka FROM tbl_product_azka ORDER BY nama_product_azka ASC")
    product_list = cursor.fetchall()

    conn.close()

    return render_template("receiving_edit_azka.html",
        username_azka=session['username_azka'],
        receiving_azka=receiving_azka,
        product_list=product_list
    )

@app.route("/receiving_delete_azka/<int:id_azka>")
def receiving_delete_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tbl_receiving_items_azka WHERE id_azka = %s", (id_azka,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Data receiving berhasil dihapus!", "success")
    return redirect(url_for("receiving_azka"))

@app.route("/receiving_addi_azka", methods=["POST"])
def receiving_addi_azka():
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    po_id_azka = request.form["po_id_azka"]
    warehouses_id_azka = request.form["warehouses_id_azka"]
    received_by_azka = request.form["received_by_azka"]
    status_azka = request.form["status_azka"]

    cursor.execute("""INSERT INTO tbl_receiving_azka 
        (po_id_azka, warehouse_id_azka, received_by_azka, status_azka)
        VALUES (%s, %s, %s, %s)""" ,(po_id_azka, warehouses_id_azka, received_by_azka, status_azka))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Data receiving berhasil ditambahkan!", "success")
    return redirect(url_for("receiving_azka"))

@app.route('/receiving_i_edit_azka/<int:id_azka>', methods=['POST'])
def receiving_i_edit_azka(id_azka):

    po_id_azka = request.form['po_id_azka']
    warehouse_id_azka = request.form['warehouse_id_azka']
    received_by_azka = request.form['received_by_azka']
    status_azka = request.form['status_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_receiving_azka
        SET po_id_azka=%s,
            warehouse_id_azka=%s,
            received_by_azka=%s,
            status_azka=%s
        WHERE id_azka=%s
    """, (po_id_azka, warehouse_id_azka, received_by_azka, status_azka, id_azka))

    conn.commit()
    conn.close()

    flash("Receiving berhasil diupdate!", "success")
    return redirect('/receiving_azka')

@app.route("/receiving_delete_i_azka/<int:id_azka>")
def receiving_delete_i_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tbl_receiving_azka WHERE id_azka = %s", (id_azka,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Data receiving berhasil dihapus!", "success")
    return redirect(url_for("receiving_azka"))


@app.route('/receiving_item_delete_azka/<int:id_azka>', methods=['GET'])
def receiving_item_delete_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tbl_receiving_items_azka WHERE id_azka=%s", (id_azka,))
    conn.commit()
    conn.close()

    flash("Barang order berhasil dihapus!", "success")
    return redirect('/receiving_azka')

@app.route('/shipment_azka')
def shipment_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

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

            u.username_azka AS courier,
            w.nama_azka AS warehouse,

            wo.latitude_azka AS origin_lat,
            wo.longitude_azka AS origin_lng,

            wl.latitude_azka AS last_lat,
            wl.longitude_azka AS last_lng
        FROM tbl_shipment_azka s


        LEFT JOIN tbl_users_azka u ON s.courier_id_azka = u.id_azka
        LEFT JOIN tbl_warehouses_azka w ON s.warehouse_id_azka = w.id_azka

        LEFT JOIN tbl_warehouses_azka wo
            ON s.warehouse_id_azka = wo.id_azka

        LEFT JOIN tbl_courier_scans_azka cs
            ON cs.id_azka = (
                SELECT id_azka FROM tbl_courier_scans_azka
                WHERE courier_id_azka = s.courier_id_azka
                ORDER BY scan_time_azka DESC
                LIMIT 1
            )

        LEFT JOIN tbl_warehouses_azka wl
            ON cs.warehouse_id_azka = wl.id_azka

        ORDER BY s.created_at_azka DESC
    """)


    data_shipment_azka = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM tbl_warehouses_azka   """)
    warehouses_azka = cursor.fetchall()
    conn.close()

    return render_template(
        'shipment_azka.html',
        data_shipment_azka=data_shipment_azka,
        warehouses_azka=warehouses_azka,
        username_azka=session['username_azka']
    )
@app.route('/shipment_add_azka', methods=['POST'])
def shipment_add_azka():
    tracking_number = "AE-" + str(int(time.time()))
    warehouse_id = request.form['warehouse_id_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # 📍 Ambil lokasi gudang asal
    cursor.execute("""
        SELECT latitude_azka, longitude_azka
        FROM tbl_warehouses_azka
        WHERE id_azka = %s
    """, (warehouse_id,))
    wh = cursor.fetchone()

    origin_lat = wh['latitude_azka']
    origin_lng = wh['longitude_azka']
    receiver_address = request.form['receiver_address_azka']

    # 📍 Ambil koordinat alamat penerima
    dest_lat, dest_lng = get_lat_lng_from_address(receiver_address)

    if dest_lat is None or dest_lng is None:
        flash("Alamat penerima tidak ditemukan di peta", "danger")
        return redirect(url_for('shipment_azka'))

    # 📦 Insert shipment (KURIR NULL)
    cursor.execute("""
        INSERT INTO tbl_shipment_azka
        (tracking_number_azka, sender_name_azka, receiver_name_azka,
        receiver_address_azka, warehouse_id_azka,
        courier_id_azka,
        origin_lat, origin_lng,
        destination_lat, destination_lng,
        last_lat, last_lng,
        status_azka)
        VALUES (%s,%s,%s,%s,%s,NULL,%s,%s,%s,%s,%s,%s,'CREATED')
    """, (
        tracking_number,
        request.form['sender_name_azka'],
        request.form['receiver_name_azka'],
        receiver_address,
        warehouse_id,
        origin_lat, origin_lng,
        dest_lat, dest_lng,          # 🎯 TUJUAN
        origin_lat, origin_lng       # posisi awal
    ))

    conn.commit()
    conn.close()

    flash("Shipment dibuat & menunggu kurir scan 📦", "success")
    return redirect(url_for('shipment_azka'))

@app.route('/shipment_pickup_azka/<int:id_azka>')
def shipment_pickup_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka='PICKED_UP',
            courier_id_azka=%s
        WHERE id_azka=%s
    """, (session['user_id_azka'], id_azka))

    conn.commit()
    conn.close()

    flash("Paket berhasil di-pickup kurir", "success")
    return redirect(url_for('shipment_azka'))

@app.route('/shipment_arrived_origin_azka/<int:id_azka>')
def shipment_arrived_origin_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka='ARRIVED_AT_ORIGIN_HUB'
        WHERE id_azka=%s
    """, (id_azka,))

    conn.commit()
    conn.close()

    flash("Barang tiba di gudang asal", "success")
    return redirect(url_for('shipment_azka'))

@app.route('/shipment_transit_azka/<int:id_azka>')
def shipment_transit_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka='IN_TRANSIT'
        WHERE id_azka=%s
    """, (id_azka,))

    conn.commit()
    conn.close()

    flash("Paket dalam proses transit", "info")
    return redirect(url_for('shipment_azka'))

@app.route('/shipment_arrived_dest_azka/<int:id_azka>')
def shipment_arrived_dest_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka='ARRIVED_AT_DEST_HUB'
        WHERE id_azka=%s
    """, (id_azka,))

    conn.commit()
    conn.close()

    flash("Barang tiba di gudang tujuan", "success")
    return redirect(url_for('shipment_azka'))

@app.route('/shipment_out_delivery_azka/<int:id_azka>')
def shipment_out_delivery_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka='OUT_FOR_DELIVERY'
        WHERE id_azka=%s
    """, (id_azka,))

    conn.commit()
    conn.close()

    flash("Paket sedang diantar kurir", "info")
    return redirect(url_for('shipment_azka'))

@app.route('/shipment_delivered_azka/<int:id_azka>')
def shipment_delivered_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka='DELIVERED'
        WHERE id_azka=%s
    """, (id_azka,))

    conn.commit()
    conn.close()

    flash("Paket berhasil diterima", "success")
    return redirect(url_for('shipment_azka'))

@app.route('/shipment_delete_azka/<int:id_azka>')
def shipment_delete_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tbl_shipment_azka WHERE id_azka=%s", (id_azka,))
    conn.commit()
    conn.close()

    flash("Shipment berhasil dihapus", "success")
    return redirect(url_for('shipment_azka'))

@app.route('/movement_azka')
def movement_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT id_azka , sku_azka, nama_product_azka FROM tbl_product_azka
    """)

    dropdown_azka = cursor.fetchall()

    cursor.execute("""
    SELECT id_azka AS location_id_azka, code_azka FROM tbl_locations_azka
    """)

    dropdown_location_azka = cursor.fetchall()    
    
    cursor.execute("""
    SELECT id_azka AS warehouse_id_azka, nama_azka FROM tbl_warehouses_azka

    """)

    dropdown_gudang_azka = cursor.fetchall()

    cursor.execute("""
    SELECT 
        s.id_azka,
        p.sku_azka,
        p.nama_product_azka,
        l.code_azka,
        w.nama_azka,
        s.quantity_azka,
        s.update_at_azka
    FROM tbl_stocks_azka s
    JOIN tbl_product_azka p ON p.id_azka = s.product_id_azka
    JOIN tbl_locations_azka l ON l.id_azka = s.location_id_azka
    JOIN tbl_warehouses_azka w ON w.id_azka = s.warehouse_id_azka
    ORDER BY s.product_id_azka ASC, s.location_id_azka ASC
""")

    data_stock_azka = cursor.fetchall()

    cursor.execute("""
    SELECT
        a.id_azka,
        b.sku_azka,
        loc_from.code_azka AS from_location_azka,
        loc_to.code_azka AS to_location_azka,
        a.quantity_azka,
        a.type_azka,
        a.reference_id_azka
    FROM
        tbl_stock_movements_azka a
    INNER JOIN tbl_product_azka b 
        ON b.id_azka = a.product_id_azka
    LEFT JOIN tbl_locations_azka loc_from 
        ON loc_from.id_azka = a.from_location_azka
    LEFT JOIN tbl_locations_azka loc_to   
        ON loc_to.id_azka = a.to_location_azka;

    
    """)
    data_stock_movement_azka = cursor.fetchall()

    conn.close()

    return render_template('movement_azka.html',
    username_azka=session['username_azka'],
        data_stock_azka=data_stock_azka,
        data_stock_movement_azka=data_stock_movement_azka,
        dropdown_azka=dropdown_azka,
        dropdown_location_azka=dropdown_location_azka,
        dropdown_gudang_azka=dropdown_gudang_azka
    )

@app.route('/stock_add_azka', methods=['POST'])
def stock_add_azka():
    product_id_azka = request.form['product_id_azka']
    location_id_azka = request.form['location_id_azka']
    warehouses_id_azka = request.form['warehouses_id_azka']
    quantity_azka = request.form['quantity_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_stocks_azka 
        (product_id_azka, location_id_azka, warehouse_id_azka, quantity_azka)
        VALUES (%s, %s, %s, %s)
    """, (product_id_azka, location_id_azka, warehouses_id_azka, quantity_azka))

    conn.commit()
    conn.close()

    flash("Data Stock berhasil ditambahkan!", "success")
    return redirect('/movement_azka')


@app.route('/stock_edit_azka/<int:id_azka>', methods=['POST'])
def stock_edit_azka(id_azka):
    product_id_azka = request.form['product_id_azka']
    location_id_azka = request.form['location_id_azka']
    warehouse_id_azka = request.form['warehouse_id_azka']
    quantity_azka = request.form['quantity_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_stocks_azka
        SET product_id_azka=%s,
            location_id_azka=%s,
            warehouse_id_azka=%s,
            quantity_azka=%s
        WHERE id_azka=%s
    """, (product_id_azka, location_id_azka, warehouse_id_azka, quantity_azka, id_azka))

    conn.commit()
    conn.close()

    flash("Data stock berhasil diperbarui!", "success")
    return redirect('/movement_azka')

@app.route('/stock_delete_azka/<int:id_azka>')
def stock_delete_azka(id_azka):

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tbl_stocks_azka WHERE id_azka=%s", (id_azka,))

    conn.commit()
    conn.close()

    flash("Data stock berhasil dihapus!", "danger")
    return redirect('/movement_azka')

@app.route('/movement_add_azka', methods=['POST'])
def movement_add_azka():
    product_id = request.form['product_id_azka']
    from_location = request.form['from_location_azka'] or None
    to_location = request.form['to_location_azka'] or None
    warehouse_id = request.form['warehouse_id_azka']
    quantity = int(request.form['quantity_azka'])
    type_move = request.form['type_azka']
    reference = request.form['reference_id_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor(buffered=True, dictionary=True)   # <<<< FIX UTAMA

    # 1 INSERT history
    cursor.execute("""
        INSERT INTO tbl_stock_movements_azka
        (product_id_azka, from_location_azka, to_location_azka, quantity_azka, type_azka, reference_id_azka)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (product_id, from_location, to_location, quantity, type_move, reference))

    # 2 UPDATE STOK
    if type_move == 'inbound':
        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka + %s
            WHERE product_id_azka = %s AND location_id_azka = %s AND warehouse_id_azka = %s
        """, (quantity, product_id, to_location, warehouse_id))

    elif type_move == 'outbound':
        cursor.execute("""
            SELECT quantity_azka FROM tbl_stocks_azka
            WHERE product_id_azka=%s AND location_id_azka=%s AND warehouse_id_azka=%s
        """, (product_id, from_location, warehouse_id))
        
        data = cursor.fetchone()

        if not data or data['quantity_azka'] < quantity:
            flash("Stok tidak cukup!", "danger")
            conn.rollback()
            conn.close()
            return redirect(url_for('movement_azka'))

        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka - %s
            WHERE product_id_azka = %s AND location_id_azka = %s AND warehouse_id_azka = %s
        """, (quantity, product_id, from_location, warehouse_id))

    elif type_move == 'transfer':
        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka - %s
            WHERE product_id_azka=%s AND location_id_azka=%s AND warehouse_id_azka=%s
        """, (quantity, product_id, from_location, warehouse_id))

        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka + %s
            WHERE product_id_azka=%s AND location_id_azka=%s AND warehouse_id_azka=%s
        """, (quantity, product_id, to_location, warehouse_id))

    conn.commit()
    conn.close()

    flash("Movement berhasil & stok diperbarui!", "success")
    return redirect(url_for('movement_azka'))

@app.route('/movement_edit_azka/<int:id>', methods=['POST'])
def movement_edit_azka(id):
    product_id_azka = request.form['product_id_azka']
    from_location_azka = request.form['from_location_azka']
    to_location_azka = request.form['to_location_azka']
    quantity_azka = request.form['quantity_azka']
    type_azka = request.form['type_azka']
    reference_id_azka = request.form['reference_id_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_stock_movements_azka
        SET product_id_azka=%s,
            from_location_azka=%s,
            to_location_azka=%s,
            quantity_azka=%s,
            type_azka=%s,
            reference_id_azka=%s
        WHERE id_azka=%s
    """, (product_id_azka,from_location_azka,to_location_azka,quantity_azka,type_azka,reference_id_azka,id
    ))

    conn.commit()
    conn.close()
    flash("Stock movement berhasil diupdate!", "success")
    return redirect(url_for('movement_azka'))

@app.route('/movement_delete_azka/<int:id>')
def movement_delete_azka(id):
    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # 1️⃣ Ambil record movement sebelum dihapus
    cursor.execute("""
        SELECT * FROM tbl_stock_movements_azka 
        WHERE id_azka = %s
    """, (id,))
    mv = cursor.fetchone()

    if not mv:
        flash("Data movement tidak ditemukan!", "danger")
        conn.close()
        return redirect(url_for('movement_azka'))

    product_id_azka = mv['product_id_azka']
    from_location_azka = mv['from_location_azka']
    to_location_azka = mv['to_location_azka']
    quantity_azka = mv['quantity_azka']
    type_azka = mv['type_azka']

    # 2️⃣ Restore stok berdasarkan tipe movement
    if type_azka == 'inbound':
        # inbound = stok bertambah → saat delete harus dikurangi
        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka - %s
            WHERE product_id_azka = %s AND location_id_azka = %s
        """, (quantity_azka, product_id_azka, to_location_azka))

    elif type_azka == 'outbound':
        # outbound = stok berkurang → saat delete harus ditambah kembali
        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka + %s
            WHERE product_id_azka = %s AND location_id_azka = %s
        """, (quantity_azka, product_id_azka, from_location_azka))

    elif type_azka == 'transfer':
        # transfer = - dari asal, + ke tujuan → saat delete kebalikannya
        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka + %s
            WHERE product_id_azka = %s AND location_id_azka = %s
        """, (quantity_azka, product_id_azka, from_location_azka))

        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka - %s
            WHERE product_id_azka = %s AND location_id_azka = %s
        """, (quantity_azka, product_id_azka, to_location_azka))

    # 3️⃣ Hapus movement
    cursor.execute("""
        DELETE FROM tbl_stock_movements_azka 
        WHERE id_azka = %s
    """, (id,))

    conn.commit()
    conn.close()

    flash("Movement dihapus dan stok dikembalikan!", "success")
    return redirect(url_for('movement_azka'))



@app.route('/suplier_azka')
def suplier_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)


    cursor.execute("""
    SELECT
    *
    FROM tbl_suppliers_azka 
    """)
    data_suplier_azka = cursor.fetchall()

    conn.close()

    return render_template('suplier_azka.html',
    username_azka=session['username_azka'],
        data_suplier_azka=data_suplier_azka
    )

@app.route('/supplier_add_azka', methods=['POST'])
def supplier_add_azka():
    nama_azka = request.form['nama_azka']
    contact_azka = request.form['contact_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_suppliers_azka 
        (nama_azka, contact_azka)
        VALUES (%s, %s)
    """, (nama_azka, contact_azka))

    conn.commit()
    conn.close()

    flash("Data Supplier berhasil ditambahkan!", "success")
    return redirect('/suplier_azka')

@app.route('/suplier_edit_azka/<int:id>', methods=['POST'])
def suplier_edit_azka(id):
    nama_azka = request.form['nama_azka']
    contact_azka = request.form['contact_azka']
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_suppliers_azka
        SET nama_azka=%s,
            contact_azka=%s
        WHERE id_azka=%s
    """, (nama_azka,contact_azka,id
    ))

    conn.commit()
    conn.close()
    flash("Stock movement berhasil diupdate!", "success")
    return redirect(url_for('suplier_azka'))

@app.route('/suplier_delete_azka/<int:id>')
def suplier_delete_azka(id):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tbl_suppliers_azka WHERE id_azka=%s", (id,))

    conn.commit()
    conn.close()
    flash("Stock movement berhasil dihapus!", "success")
    return redirect(url_for('suplier_azka'))

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

    # ================= TOTAL =================
    cursor.execute("SELECT COALESCE(SUM(quantity_received_azka), 0) total FROM tbl_receiving_items_azka")
    total_barang_masuk = cursor.fetchone()['total']

    cursor.execute("SELECT COALESCE(SUM(quantity_azka), 0) total FROM tbl_order_items_azka")
    total_barang_keluar = cursor.fetchone()['total']

    cursor.execute("SELECT COALESCE(SUM(quantity_azka), 0) total FROM tbl_stocks_azka")
    total_stok = cursor.fetchone()['total']

    # ================= STOK PRODUK =================
    cursor.execute("""
        SELECT p.nama_product_azka AS nama_produk,
        COALESCE(SUM(s.quantity_azka), 0) AS total_stok
        FROM tbl_product_azka p
        LEFT JOIN tbl_stocks_azka s ON s.product_id_azka = p.id_azka
        GROUP BY p.id_azka, p.nama_product_azka
    """)
    stok_per_produk = cursor.fetchall()

    # ================= STOK GUDANG =================
    cursor.execute("""
        SELECT w.nama_azka AS gudang,
        COALESCE(SUM(s.quantity_azka), 0) AS total_stok
        FROM tbl_warehouses_azka w
        LEFT JOIN tbl_stocks_azka s ON s.warehouse_id_azka = w.id_azka
        GROUP BY w.id_azka, w.nama_azka
    """)
    stok_per_gudang = cursor.fetchall()

    # ================= GRAFIK BULANAN =================
    cursor.execute("""
        SELECT MONTH(created_at_azka) AS bulan_angka,
        DATE_FORMAT(created_at_azka, '%b') AS bulan,
        SUM(quantity_received_azka) AS total
        FROM tbl_receiving_items_azka
        GROUP BY bulan_angka, bulan
        ORDER BY bulan_angka
    """)
    masuk = cursor.fetchall()

    cursor.execute("""
        SELECT MONTH(created_at_azka) AS bulan_angka,
        DATE_FORMAT(created_at_azka, '%b') AS bulan,
        SUM(quantity_azka) AS total
        FROM tbl_order_items_azka
        GROUP BY bulan_angka, bulan
        ORDER BY bulan_angka
    """)
    keluar = cursor.fetchall()

    semua_bulan = sorted(set([m['bulan'] for m in masuk] + [k['bulan'] for k in keluar]))

    data_masuk = [next((m['total'] for m in masuk if m['bulan'] == b), 0) for b in semua_bulan]
    data_keluar = [next((k['total'] for k in keluar if k['bulan'] == b), 0) for b in semua_bulan]

    conn.close()

    return render_template(
        'gudang_dashboard_azka.html',
        username_azka=session['username_azka'],

        total_barang_masuk=total_barang_masuk,
        total_barang_keluar=total_barang_keluar,
        total_stok=total_stok,

        labels_bulanan=semua_bulan,
        data_masuk_bulanan=data_masuk,
        data_keluar_bulanan=data_keluar,

        stok_per_produk=stok_per_produk,
        stok_per_gudang=stok_per_gudang
    )


@app.route('/gudang_expired_azka')
def gudang_expired_azka():
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
        r.id_azka,
        p.nama_product_azka,
        r.batch_number_azka,
        r.expire_date_azka,
        r.quantity_accepted_azka
    FROM tbl_receiving_items_azka r
    INNER JOIN tbl_product_azka p ON r.product_id_azka = p.id_azka
    WHERE r.expire_date_azka BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
    ORDER BY r.expire_date_azka ASC;

    """)

    data_expired_azka = cursor.fetchall()
    conn.close()

    return render_template("gudang_expired_azka.html",
                           username_azka=session['username_azka'],
                           data_expired_azka=data_expired_azka)
@app.route('/gudang_lowstock_azka', methods=['GET', 'POST'])
def gudang_lowstock_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in (1, 2):
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    selected_warehouse = request.form.get("warehouse_id_azka")

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # Dropdown gudang
    cursor.execute("SELECT id_azka, nama_azka FROM tbl_warehouses_azka")
    warehouses_azka = cursor.fetchall()

    # ================================
    # 🔥 FIX QUERY TOTAL STOK SESUAI DB
    # ================================
    if selected_warehouse:
        cursor.execute("""
            SELECT 
                p.id_azka,
                p.sku_azka,
                p.nama_product_azka,
                p.min_stock_azka,
                IFNULL(SUM(s.quantity_azka), 0) AS total_stok_azka
            FROM tbl_product_azka p
            LEFT JOIN tbl_stocks_azka s 
                ON s.product_id_azka = p.id_azka
                AND s.warehouse_id_azka = %s
            GROUP BY p.id_azka, p.sku_azka, p.nama_product_azka, p.min_stock_azka
            ORDER BY total_stok_azka ASC
        """, (selected_warehouse,))
    else:
        cursor.execute("""
            SELECT 
                p.id_azka,
                p.sku_azka,
                p.nama_product_azka,
                p.min_stock_azka,
                IFNULL(SUM(s.quantity_azka), 0) AS total_stok_azka
            FROM tbl_product_azka p
            LEFT JOIN tbl_stocks_azka s 
                ON s.product_id_azka = p.id_azka
            GROUP BY p.id_azka, p.sku_azka, p.nama_product_azka, p.min_stock_azka
            ORDER BY total_stok_azka ASC
        """)

    low_stock_azka = cursor.fetchall()

    # Tabel data barang (produk)
    cursor.execute("""
        SELECT 
            l.id_azka,
            l.sku_azka,
            l.nama_product_azka,
            u.nama_azka AS category_name,
            l.category_id_azka,
            l.unit_azka,
            l.min_stock_azka
        FROM tbl_product_azka l
        INNER JOIN tbl_product_categories_azka u
            ON l.category_id_azka = u.id_azka
        ORDER BY l.id_azka DESC
    """)
    product_azka = cursor.fetchall()

    # Kategori produk
    cursor.execute("SELECT id_azka, nama_azka FROM tbl_product_categories_azka ORDER BY id_azka ASC")
    categories = cursor.fetchall()

    conn.close()

    return render_template(
        "gudang_lowstock_azka.html",
        username_azka=session['username_azka'],
        low_stock_azka=low_stock_azka,
        warehouses_azka=warehouses_azka,
        selected_warehouse=selected_warehouse,
        product_azka=product_azka,
        categories=categories
    )

@app.route('/low_product_add_azka', methods=['POST'])
def low_product_add_azka():
    sku_azka = request.form['sku_azka']
    nama_product_azka = request.form['nama_product_azka']
    category_id_azka = request.form['category_id_azka']
    unit_azka = request.form['unit_azka']
    min_stock_azka = request.form['min_stock_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_product_azka 
        (sku_azka, nama_product_azka, category_id_azka, unit_azka, min_stock_azka)
        VALUES (%s, %s, %s, %s, %s)
    """, (sku_azka, nama_product_azka, category_id_azka, unit_azka, min_stock_azka))

    conn.commit()
    conn.close()

    insert_log_azka(session['user_id_azka'], "Tambah Data", f"Barang #{sku_azka} di tambahkan")
    flash("Berhasil menambah data barang!", "success")
    return redirect(url_for('gudang_lowstock_azka'))

@app.route('/low_product_edit_azka/<int:id_azka>', methods=['GET', 'POST'])
def low_product_edit_azka(id_azka):
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
            UPDATE tbl_product_azka SET
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
        return redirect(url_for('gudang_lowstock_azka'))

    cursor.execute("SELECT * FROM tbl_product_azka WHERE id_azka=%s", (id_azka,))
    product = cursor.fetchone()

    cursor.execute("SELECT * FROM tbl_product_categories_azka")
    categories = cursor.fetchall()

    conn.close()

    return render_template(
        "gudang_lowstock_azka.html",
        product=product,
        categories=categories,
        username_azka=session['username_azka']
    )

@app.route('/low_product_delete_azka/<int:id_azka>', methods=['GET'])
def low_product_delete_azka(id_azka):
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("SELECT nama_azka FROM tbl_product_azka WHERE id_azka=%s", (id_azka,))
    row = cursor.fetchone()
    nama_barang = row[0] if row else "Tidak diketahui"

    cursor.execute("DELETE FROM tbl_product_azka WHERE id_azka=%s", (id_azka,))
    conn.commit()

    conn.close()

    insert_log_azka(session['user_id_azka'], "Delete", f"Hapus barang: {nama_barang}")

    flash("Barang berhasil dihapus!", "danger")
    return redirect(url_for('gudang_lowstock_azka'))

@app.route('/gudang_mutasi_azka')
def gudang_mutasi_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in (1, 2):
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # =======================
    #  DROPDOWN PRODUK
    # =======================
    cursor.execute("""
        SELECT id_azka, sku_azka, nama_product_azka 
        FROM tbl_product_azka
    """)
    dropdown_azka = cursor.fetchall()

    # =======================
    #  DROPDOWN LOKASI
    # =======================
    cursor.execute("""
        SELECT id_azka AS location_id_azka, code_azka 
        FROM tbl_locations_azka
    """)
    dropdown_location_azka = cursor.fetchall()

    # =======================
    #  DROPDOWN GUDANG
    # =======================
    cursor.execute("""
        SELECT id_azka AS warehouse_id_azka, nama_azka 
        FROM tbl_warehouses_azka
    """)
    dropdown_gudang_azka = cursor.fetchall()

    # =======================
    #  DATA MUTASI
    # =======================
    cursor.execute("""
        SELECT
            m.id_azka,
            p.nama_product_azka,
            m.quantity_azka,
            m.type_azka,
            m.reference_id_azka,
            lf.code_azka AS from_location_azka,
            lt.code_azka AS to_location_azka,
            m.created_at_azka
        FROM tbl_stock_movements_azka m
        INNER JOIN tbl_product_azka p 
            ON p.id_azka = m.product_id_azka
        LEFT JOIN tbl_locations_azka lf 
            ON lf.id_azka = m.from_location_azka
        LEFT JOIN tbl_locations_azka lt 
            ON lt.id_azka = m.to_location_azka
        ORDER BY m.created_at_azka DESC
    """)
    mutasi_azka = cursor.fetchall()

    conn.close()

    return render_template("gudang_mutasi_azka.html",
                           username_azka=session['username_azka'],
                           mutasi_azka=mutasi_azka,
                           dropdown_azka=dropdown_azka,
                           dropdown_location_azka=dropdown_location_azka,
                           dropdown_gudang_azka=dropdown_gudang_azka)


@app.route('/gudang_stock_add_azka', methods=['POST'])
def gudang_stock_add_azka():
    product_id = request.form['product_id_azka']
    from_location = request.form['from_location_azka'] or None
    to_location = request.form['to_location_azka'] or None
    warehouse_id = request.form['warehouse_id_azka']
    quantity = int(request.form['quantity_azka'])
    type_move = request.form['type_azka']
    reference = request.form['reference_id_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor(buffered=True, dictionary=True)   # <<<< FIX UTAMA

    # 1 INSERT history
    cursor.execute("""
        INSERT INTO tbl_stock_movements_azka
        (product_id_azka, from_location_azka, to_location_azka, quantity_azka, type_azka, reference_id_azka)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (product_id, from_location, to_location, quantity, type_move, reference))

    # 2 UPDATE STOK
    if type_move == 'inbound':
        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka + %s
            WHERE product_id_azka = %s AND location_id_azka = %s AND warehouse_id_azka = %s
        """, (quantity, product_id, to_location, warehouse_id))

    elif type_move == 'outbound':
        cursor.execute("""
            SELECT quantity_azka FROM tbl_stocks_azka
            WHERE product_id_azka=%s AND location_id_azka=%s AND warehouse_id_azka=%s
        """, (product_id, from_location, warehouse_id))
        
        data = cursor.fetchone()

        if not data or data['quantity_azka'] < quantity:
            flash("Stok tidak cukup!", "danger")
            conn.rollback()
            conn.close()
            return redirect(url_for('gudang_mutasi_azka'))

        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka - %s
            WHERE product_id_azka = %s AND location_id_azka = %s AND warehouse_id_azka = %s
        """, (quantity, product_id, from_location, warehouse_id))

    elif type_move == 'transfer':
        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka - %s
            WHERE product_id_azka=%s AND location_id_azka=%s AND warehouse_id_azka=%s
        """, (quantity, product_id, from_location, warehouse_id))

        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka + %s
            WHERE product_id_azka=%s AND location_id_azka=%s AND warehouse_id_azka=%s
        """, (quantity, product_id, to_location, warehouse_id))

    conn.commit()
    conn.close()

    flash("Movement berhasil & stok diperbarui!", "success")
    return redirect(url_for('gudang_mutasi_azka'))

@app.route('/gudang_stock_edit_azka/<int:id>', methods=['POST'])
def gudang_stock_edit_azka(id):
    product_id_azka = request.form['product_id_azka']
    from_location_azka = request.form['from_location_azka']
    to_location_azka = request.form['to_location_azka']
    quantity_azka = request.form['quantity_azka']
    type_azka = request.form['type_azka']
    reference_id_azka = request.form['reference_id_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_stock_movements_azka
        SET product_id_azka=%s,
            from_location_azka=%s,
            to_location_azka=%s,
            quantity_azka=%s,
            type_azka=%s,
            reference_id_azka=%s
        WHERE id_azka=%s
    """, (product_id_azka,from_location_azka,to_location_azka,quantity_azka,type_azka,reference_id_azka,id
    ))

    conn.commit()
    conn.close()
    flash("Stock movement berhasil diupdate!", "success")
    return redirect(url_for('gudang_mutasi_azka'))

@app.route('/gudang_delete_stock_azka/<int:id>')
def gudang_delete_stock_azka(id):
    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # 1️⃣ Ambil record movement sebelum dihapus
    cursor.execute("""
        SELECT * FROM tbl_stock_movements_azka 
        WHERE id_azka = %s
    """, (id,))
    mv = cursor.fetchone()

    if not mv:
        flash("Data movement tidak ditemukan!", "danger")
        conn.close()
        return redirect(url_for('movement_azka'))

    product_id_azka = mv['product_id_azka']
    from_location_azka = mv['from_location_azka']
    to_location_azka = mv['to_location_azka']
    quantity_azka = mv['quantity_azka']
    type_azka = mv['type_azka']

    # 2️⃣ Restore stok berdasarkan tipe movement
    if type_azka == 'inbound':
        # inbound = stok bertambah → saat delete harus dikurangi
        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka - %s
            WHERE product_id_azka = %s AND location_id_azka = %s
        """, (quantity_azka, product_id_azka, to_location_azka))

    elif type_azka == 'outbound':
        # outbound = stok berkurang → saat delete harus ditambah kembali
        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka + %s
            WHERE product_id_azka = %s AND location_id_azka = %s
        """, (quantity_azka, product_id_azka, from_location_azka))

    elif type_azka == 'transfer':
        # transfer = - dari asal, + ke tujuan → saat delete kebalikannya
        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka + %s
            WHERE product_id_azka = %s AND location_id_azka = %s
        """, (quantity_azka, product_id_azka, from_location_azka))

        cursor.execute("""
            UPDATE tbl_stocks_azka
            SET quantity_azka = quantity_azka - %s
            WHERE product_id_azka = %s AND location_id_azka = %s
        """, (quantity_azka, product_id_azka, to_location_azka))

    # 3️⃣ Hapus movement
    cursor.execute("""
        DELETE FROM tbl_stock_movements_azka 
        WHERE id_azka = %s
    """, (id,))

    conn.commit()
    conn.close()

    flash("Movement dihapus dan stok dikembalikan!", "success")
    return redirect(url_for('gudang_mutasi_azka'))

@app.route('/gudang_laporan_azka')
def gudang_laporan_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in (1, 2):

        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT COALESCE(SUM(ri.quantity_received_azka), 0) AS total_barang_masuk
        FROM tbl_receiving_items_azka ri
    """)
    total_barang_masuk = cursor.fetchone()['total_barang_masuk']

    # Total Barang Keluar
    cursor.execute("""
        SELECT COALESCE(SUM(oi.quantity_azka), 0) AS total_barang_keluar
        FROM tbl_order_items_azka oi
    """)
    total_barang_keluar = cursor.fetchone()['total_barang_keluar']

    # Total Stok
    cursor.execute("""
        SELECT COALESCE(SUM(s.quantity_azka), 0) AS total_stok
        FROM tbl_stocks_azka s
    """)
    total_stok = cursor.fetchone()['total_stok']

    # Barang Masuk (receiving items) - tampil detail penting
    cursor.execute("""
        SELECT 
            ri.id_azka,
            p.nama_product_azka,
            ri.batch_number_azka,
            ri.expire_date_azka,
            ri.quantity_received_azka,
            ri.created_at_azka
        FROM tbl_receiving_items_azka ri
        INNER JOIN tbl_product_azka p ON p.id_azka = ri.product_id_azka
        ORDER BY ri.created_at_azka DESC
    """)
    barang_masuk_azka = cursor.fetchall()

    # Barang Keluar (order items) - tampil detail penting
    cursor.execute("""
       SELECT 
            oi.id_azka,
            p.nama_product_azka,
            a.order_number_azka,
            oi.quantity_azka,
            oi.created_at_azka
        FROM tbl_order_items_azka oi
        INNER JOIN tbl_product_azka p ON p.id_azka = oi.product_id_azka
        INNER JOIN tbl_orders_azka a ON a.id_azka = oi.order_id_azka
        ORDER BY oi.created_at_azka DESC;
    """)
    barang_keluar_azka = cursor.fetchall()

    conn.close()

    return render_template(
        "gudang_laporan_azka.html",
        username_azka=session['username_azka'],
        barang_masuk_azka=barang_masuk_azka,
        barang_keluar_azka=barang_keluar_azka,
        total_barang_masuk=total_barang_masuk,
        total_barang_keluar=total_barang_keluar,
        total_stok=total_stok

    )



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



@app.route('/gudang_stock_azka')
def gudang_stock_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in (1, 2):
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT id_azka , sku_azka, nama_product_azka FROM tbl_product_azka
    """)

    dropdown_azka = cursor.fetchall()

    cursor.execute("""
    SELECT id_azka AS location_id_azka, code_azka FROM tbl_locations_azka
    """)

    dropdown_location_azka = cursor.fetchall()    
    
    cursor.execute("""
    SELECT id_azka AS warehouse_id_azka, nama_azka FROM tbl_warehouses_azka

    """)

    dropdown_gudang_azka = cursor.fetchall()

    cursor.execute("""
        SELECT 
            s.id_azka AS id_stock_azka,
            p.id_azka AS id_produk_azka,
            w.id_azka AS id_gudang_azka,
            p.sku_azka,
            p.nama_product_azka,
            l.code_azka AS lokasi_azka,
            w.nama_azka AS gudang_azka,
            s.quantity_azka,
            s.update_at_azka
        FROM tbl_stocks_azka s
        INNER JOIN tbl_product_azka p ON p.id_azka = s.product_id_azka
        INNER JOIN tbl_locations_azka l ON l.id_azka = s.location_id_azka
        INNER JOIN tbl_warehouses_azka w ON w.id_azka = s.warehouse_id_azka
        ORDER BY p.nama_product_azka ASC, l.code_azka ASC
    """)

    stock_azka = cursor.fetchall()

    conn.close()

    return render_template(
        "gudang_stock_azka.html",
        username_azka=session['username_azka'],
        stock_azka=stock_azka,
        dropdown_gudang_azka=dropdown_gudang_azka,
        dropdown_location_azka=dropdown_location_azka,
        dropdown_azka=dropdown_azka

    )

@app.route('/gudang_stocks_add_azka', methods=['POST'])
def gudang_stocks_add_azka():
    product_id_azka = request.form['product_id_azka']
    location_id_azka = request.form['location_id_azka']
    warehouses_id_azka = request.form['warehouses_id_azka']
    quantity_azka = request.form['quantity_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_stocks_azka 
        (product_id_azka, location_id_azka, warehouse_id_azka, quantity_azka)
        VALUES (%s, %s, %s, %s)
    """, (product_id_azka, location_id_azka, warehouses_id_azka, quantity_azka))

    conn.commit()
    conn.close()

    flash("Data Stock berhasil ditambahkan!", "success")
    return redirect('/gudang_stock_azka')


@app.route('/gudang_stocks_edit_azka/<int:id_azka>', methods=['POST'])
def gudang_stocks_edit_azka(id_azka):
    product_id_azka = request.form['product_id_azka']
    location_id_azka = request.form['location_id_azka']
    warehouse_id_azka = request.form['warehouse_id_azka']
    quantity_azka = request.form['quantity_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_stocks_azka
        SET product_id_azka=%s,
            location_id_azka=%s,
            warehouse_id_azka=%s,
            quantity_azka=%s
        WHERE id_azka=%s
    """, (product_id_azka, location_id_azka, warehouse_id_azka, quantity_azka, id_azka))

    conn.commit()
    conn.close()

    flash("Data stock berhasil diperbarui!", "success")
    return redirect('/gudang_stock_azka')

@app.route('/gudang_stocks_delete_azka/<int:id_azka>')
def gudang_stocks_delete_azka(id_azka):

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tbl_stocks_azka WHERE id_azka=%s", (id_azka,))

    conn.commit()
    conn.close()

    flash("Data stock berhasil dihapus!", "danger")
    return redirect('/gudang_stock_azka')

@app.route('/gudang_masuk_azka')
def gudang_masuk_azka():
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
        a.id_azka,
        a.product_id_azka,
        b.nama_product_azka,
        a.batch_number_azka,
        a.quantity_received_azka,
        a.quantity_accepted_azka,
        a.expire_date_azka
    FROM
        tbl_receiving_items_azka a
    INNER JOIN tbl_product_azka b ON
        a.product_id_azka = b.id_azka
    ORDER BY a.id_azka ASC;
    """)

    receiving_azka = cursor.fetchall()
    
    cursor.execute("SELECT id_azka, nama_product_azka FROM tbl_product_azka ")
    product_list = cursor.fetchall()

    cursor.execute("SELECT id_azka, status_azka FROM tbl_receiving_azka ")
    status_azka = cursor.fetchall()

    cursor.execute("""
    SELECT
        a.id_azka,
        a.po_id_azka,
        a.warehouse_id_azka,
        a.received_by_azka,
        a.status_azka,

        b.nama_azka AS warehouse_name,
        c.po_number_azka,
        d.username_azka
    FROM tbl_receiving_azka a
    LEFT JOIN tbl_warehouses_azka b ON a.warehouse_id_azka = b.id_azka
    LEFT JOIN tbl_purchase_orders_azka c ON a.po_id_azka = c.id_azka
    LEFT JOIN tbl_users_azka d ON a.received_by_azka = d.id_azka;
    """)
    rece_azka = cursor.fetchall()

    cursor.execute("SELECT id_azka, po_number_azka FROM tbl_purchase_orders_azka")
    dropdown_po = cursor.fetchall()

    cursor.execute("SELECT id_azka, nama_azka FROM tbl_warehouses_azka")
    dropdown_gudang = cursor.fetchall()

    cursor.execute("SELECT id_azka, username_azka FROM tbl_users_azka")
    dropdown_users_azka = cursor.fetchall()


    conn.close()

    return render_template(
    "gudang_masuk_azka.html",
    username_azka=session['username_azka'],
    receiving_azka=receiving_azka,
    product_list=product_list,
    rece_azka=rece_azka,
    status_azka=status_azka,
    dropdown_po=dropdown_po,
    dropdown_gudang=dropdown_gudang,
    dropdown_users_azka=dropdown_users_azka
)

@app.route('/gudang_masuk_add_azka', methods=['POST'])
def gudang_masuk_add_azka():
    receiving_id_azka = request.form['receiving_id_azka']
    product_id_azka = request.form['product_id_azka']
    batch_number_azka = request.form['batch_number_azka']
    quantity_received_azka = request.form['quantity_received_azka']
    quantity_accepted_azka = request.form['quantity_accepted_azka']
    expire_date_azka = request.form['expire_date_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_receiving_items_azka 
        (receiving_id_azka, product_id_azka, batch_number_azka, quantity_received_azka,quantity_accepted_azka,expire_date_azka)
        VALUES (%s, %s, %s, %s,%s,%s)
    """, (receiving_id_azka, product_id_azka, batch_number_azka, quantity_received_azka,quantity_accepted_azka,expire_date_azka))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Data barang masuk berhasil ditambahkan!", "success")
    return redirect('/gudang_masuk_azka')

@app.route('/gudang_masuk_edit_azka/<int:id_azka>', methods=['GET', 'POST'])
def gudang_masuk_edit_azka(id_azka):
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in [1, 2]:
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        product_id_azka = request.form['product_id_azka']
        batch_number_azka = request.form['batch_number_azka']
        quantity_received_azka = request.form['quantity_received_azka']
        quantity_accepted_azka = request.form['quantity_accepted_azka']
        expire_date_azka = request.form['expire_date_azka']

        cursor.execute("""
            UPDATE tbl_receiving_items_azka SET
                product_id_azka = %s,
                batch_number_azka = %s,
                quantity_received_azka = %s,
                quantity_accepted_azka = %s,
                expire_date_azka = %s
            WHERE id_azka = %s
        """, (product_id_azka, batch_number_azka, quantity_received_azka,
              quantity_accepted_azka, expire_date_azka, id_azka))
        conn.commit()

        conn.close()

        insert_log_azka(session['user_id_azka'], "Edit Receiving",
                        f"Receiving ID {id_azka} diperbarui")

        flash("Data receiving berhasil diperbarui!", "success")
        return redirect(url_for('receiving_azka'))

    cursor.execute("""
        SELECT 
            r.*, p.nama_product_azka
        FROM tbl_receiving_items_azka r
        INNER JOIN tbl_product_azka p 
            ON r.product_id_azka = p.id_azka
        WHERE r.id_azka = %s
    """, (id_azka,))
    receiving_azka = cursor.fetchone()


    cursor.execute("SELECT id_azka, nama_product_azka FROM tbl_product_azka ORDER BY nama_product_azka ASC")
    product_list = cursor.fetchall()

    conn.close()

    return render_template("gudang_masuk_azka.html",
        username_azka=session['username_azka'],
        receiving_azka=receiving_azka,
        product_list=product_list
    )

@app.route("/gudang_masuk_delete_azka/<int:id_azka>")
def gudang_masuk_delete_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tbl_receiving_items_azka WHERE id_azka = %s", (id_azka,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Data receiving berhasil dihapus!", "success")
    return redirect(url_for("gudang_masuk_azka"))

@app.route("/gudang_masuk_addi_azka", methods=["POST"])
def gudang_masuk_addi_azka():
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    po_id_azka = request.form["po_id_azka"]
    warehouses_id_azka = request.form["warehouses_id_azka"]
    received_by_azka = request.form["received_by_azka"]
    status_azka = request.form["status_azka"]

    cursor.execute("""INSERT INTO tbl_receiving_azka 
        (po_id_azka, warehouse_id_azka, received_by_azka, status_azka)
        VALUES (%s, %s, %s, %s)""" ,(po_id_azka, warehouses_id_azka, received_by_azka, status_azka))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Data receiving berhasil ditambahkan!", "success")
    return redirect(url_for("gudang_masuk_azka"))

@app.route('/gudang_masuk_i_edit_azka/<int:id_azka>', methods=['POST'])
def gudang_masuk_i_edit_azka(id_azka):

    po_id_azka = request.form['po_id_azka']
    warehouse_id_azka = request.form['warehouse_id_azka']
    received_by_azka = request.form['received_by_azka']
    status_azka = request.form['status_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_receiving_azka
        SET po_id_azka=%s,
            warehouse_id_azka=%s,
            received_by_azka=%s,
            status_azka=%s
        WHERE id_azka=%s
    """, (po_id_azka, warehouse_id_azka, received_by_azka, status_azka, id_azka))

    conn.commit()
    conn.close()

    flash("Receiving berhasil diupdate!", "success")
    return redirect('/gudang_masuk_azka')

@app.route("/gudang_masuk_delete_i_azka/<int:id_azka>")
def gudang_masuk_delete_i_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tbl_receiving_azka WHERE id_azka = %s", (id_azka,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Data receiving berhasil dihapus!", "success")
    return redirect(url_for("receiving_azka"))


@app.route('/gudang_masuk_item_delete_azka/<int:id_azka>', methods=['GET'])
def gudang_masuk_item_delete_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tbl_receiving_items_azka WHERE id_azka=%s", (id_azka,))
    conn.commit()
    conn.close()

    flash("Barang order berhasil dihapus!", "success")
    return redirect('/gudang_masuk_azka')

@app.route('/gudang_keluar_azka')
def gudang_keluar_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in (1, 2):
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT * FROM tbl_orders_azka
    """)
    data_order_azka = cursor.fetchall()

    cursor.execute("""
    SELECT
        a.id_azka AS order_item_id,
        a.order_id_azka,
        a.product_id_azka,
        a.quantity_azka,

        b.order_number_azka,
        b.customer_nama_azka,

        c.nama_product_azka,
        c.sku_azka
    FROM tbl_order_items_azka a
    INNER JOIN tbl_orders_azka b ON a.order_id_azka = b.id_azka
    INNER JOIN tbl_product_azka c ON a.product_id_azka = c.id_azka
    """)
    data_barang_azka = cursor.fetchall()

    cursor.execute("SELECT id_azka, sku_azka FROM tbl_product_azka")
    dropdown_barang_azka = cursor.fetchall()
    conn.close()

    return render_template('gudang_keluar_azka.html',
    username_azka=session['username_azka'],
        data_order_azka=data_order_azka,
        data_barang_azka=data_barang_azka,
        dropdown_barang_azka=dropdown_barang_azka
    )

@app.route('/gudang_keluar_item_add_azka', methods=['POST'])
def gudang_keluar_item_add_azka():
    order_id_azka = request.form['order_id_azka']
    product_id_azka = request.form['product_id_azka']
    quantity_azka = int(request.form['quantity_azka'])

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # 1️⃣ CEK STOK TERSEDIA
    cursor.execute("""
        SELECT quantity_azka
        FROM tbl_stocks_azka
        WHERE product_id_azka = %s
        LIMIT 1
    """, (product_id_azka,))
    stock_data = cursor.fetchone()

    if not stock_data:
        conn.close()
        flash("Stok tidak ditemukan!", "danger")
        return redirect('/gudang_keluar_azka')

    stok_sekarang = stock_data['quantity_azka']

    # 2️⃣ CEK STOK CUKUP
    if stok_sekarang < quantity_azka:
        conn.close()
        flash("Stok tidak mencukupi!", "danger")
        return redirect('/gudang_keluar_azka')

    # 3️⃣ INSERT ORDER ITEM
    cursor.execute("""
        INSERT INTO tbl_order_items_azka
        (order_id_azka, product_id_azka, quantity_azka)
        VALUES (%s, %s, %s)
    """, (order_id_azka, product_id_azka, quantity_azka))

    # 4️⃣ KURANGI STOK
    cursor.execute("""
        UPDATE tbl_stocks_azka
        SET quantity_azka = quantity_azka - %s
        WHERE product_id_azka = %s
    """, (quantity_azka, product_id_azka))

    conn.commit()
    conn.close()

    flash("Barang berhasil ditambahkan & stok berkurang!", "success")
    return redirect('/gudang_keluar_azka')



@app.route('/gudang_keluar_item_edit_azka/<int:id_azka>', methods=['POST'])
def gudang_keluar_item_edit_azka(id_azka):
    order_id_azka = request.form['order_id_azka']
    product_id_azka = request.form['product_id_azka']
    quantity_azka = request.form['quantity_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_order_items_azka
        SET order_id_azka=%s,product_id_azka=%s, quantity_azka=%s
        WHERE id_azka=%s
    """, (order_id_azka,product_id_azka, quantity_azka, id_azka))

    conn.commit()
    conn.close()

    flash("Data barang berhasil diupdate!", "success")
    return redirect('/gudang_keluar_azka')

@app.route('/gudang_azka_item_delete_azka/<int:id_azka>', methods=['GET'])
def gudang_azka_item_delete_azka(id_azka):
    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT product_id_azka, quantity_azka
        FROM tbl_order_items_azka
        WHERE id_azka=%s
    """, (id_azka,))
    item = cursor.fetchone()

    cursor.execute("""
        UPDATE tbl_stocks_azka
        SET quantity_azka = quantity_azka + %s
        WHERE product_id_azka = %s
    """, (item['quantity_azka'], item['product_id_azka']))

    cursor.execute("""
        DELETE FROM tbl_order_items_azka WHERE id_azka=%s
    """, (id_azka,))

    conn.commit()
    conn.close()

    flash("Barang dihapus & stok dikembalikan!", "success")
    return redirect('/gudang_keluar_azka')


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

@app.route('/manager_update_shipment_status_azka/<int:shipment_id>/<string:new_status>')
def manager_update_shipment_status_azka(shipment_id, new_status):
    if 'user_id_azka' not in session:
        return "Unauthorized", 403

    if session['role_id_azka'] not in [1, 4]:
        return "Forbidden", 403

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka=%s
        WHERE id_azka=%s
    """, (new_status, shipment_id))

    conn.commit()
    conn.close()

    return "OK"


# ---------------------------
# 3) Stock Monitor (stok rendah, in/out summary)
# ---------------------------
@app.route('/manager_stock_monitor_azka', methods=['GET', 'POST'])
def manager_stock_monitor_azka():
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    if session.get('role_id_azka') not in (1, 2):
        flash("Akses ditolak!", "danger")
        return redirect(url_for('dashboard_azka'))

    selected_warehouse = request.form.get("warehouse_id_azka")

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # Dropdown gudang
    cursor.execute("SELECT id_azka, nama_azka FROM tbl_warehouses_azka")
    warehouses_azka = cursor.fetchall()

    # ================================
    # 🔥 FIX QUERY TOTAL STOK SESUAI DB
    # ================================
    if selected_warehouse:
        cursor.execute("""
            SELECT 
                p.id_azka,
                p.sku_azka,
                p.nama_product_azka,
                p.min_stock_azka,
                IFNULL(SUM(s.quantity_azka), 0) AS total_stok_azka
            FROM tbl_product_azka p
            LEFT JOIN tbl_stocks_azka s 
                ON s.product_id_azka = p.id_azka
                AND s.warehouse_id_azka = %s
            GROUP BY p.id_azka, p.sku_azka, p.nama_product_azka, p.min_stock_azka
            ORDER BY total_stok_azka ASC
        """, (selected_warehouse,))
    else:
        cursor.execute("""
            SELECT 
                p.id_azka,
                p.sku_azka,
                p.nama_product_azka,
                p.min_stock_azka,
                IFNULL(SUM(s.quantity_azka), 0) AS total_stok_azka
            FROM tbl_product_azka p
            LEFT JOIN tbl_stocks_azka s 
                ON s.product_id_azka = p.id_azka
            GROUP BY p.id_azka, p.sku_azka, p.nama_product_azka, p.min_stock_azka
            ORDER BY total_stok_azka ASC
        """)

    low_stock_azka = cursor.fetchall()

    # Tabel data barang (produk)
    cursor.execute("""
        SELECT 
            l.id_azka,
            l.sku_azka,
            l.nama_product_azka,
            u.nama_azka AS category_name,
            l.category_id_azka,
            l.unit_azka,
            l.min_stock_azka
        FROM tbl_product_azka l
        INNER JOIN tbl_product_categories_azka u
            ON l.category_id_azka = u.id_azka
        ORDER BY l.id_azka DESC
    """)
    product_azka = cursor.fetchall()

    # Kategori produk
    cursor.execute("SELECT id_azka, nama_azka FROM tbl_product_categories_azka ORDER BY id_azka ASC")
    categories = cursor.fetchall()

    conn.close()

    return render_template(
        "manager_stock_monitor_azka.html",
        username_azka=session['username_azka'],
        low_stock_azka=low_stock_azka,
        warehouses_azka=warehouses_azka,
        selected_warehouse=selected_warehouse,
        product_azka=product_azka,
        categories=categories
    )
@app.route('/manager_low_product_add_azka', methods=['POST'])
def manager_low_product_add_azka():
    sku_azka = request.form['sku_azka']
    nama_product_azka = request.form['nama_product_azka']
    category_id_azka = request.form['category_id_azka']
    unit_azka = request.form['unit_azka']
    min_stock_azka = request.form['min_stock_azka']

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_product_azka 
        (sku_azka, nama_product_azka, category_id_azka, unit_azka, min_stock_azka)
        VALUES (%s, %s, %s, %s, %s)
    """, (sku_azka, nama_product_azka, category_id_azka, unit_azka, min_stock_azka))

    conn.commit()
    conn.close()

    insert_log_azka(session['user_id_azka'], "Tambah Data", f"Barang #{sku_azka} di tambahkan")
    flash("Berhasil menambah data barang!", "success")
    return redirect(url_for('manager_stock_monitor_azka'))

@app.route('/manager_low_product_edit_azka/<int:id_azka>', methods=['GET', 'POST'])
def manager_low_product_edit_azka(id_azka):
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
            UPDATE tbl_product_azka SET
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
        return redirect(url_for('gudang_lowstock_azka'))

    cursor.execute("SELECT * FROM tbl_product_azka WHERE id_azka=%s", (id_azka,))
    product = cursor.fetchone()

    cursor.execute("SELECT * FROM tbl_product_categories_azka")
    categories = cursor.fetchall()

    conn.close()

    return render_template(
        "manager_stock_monitor_azka.html",
        product=product,
        categories=categories,
        username_azka=session['username_azka']
    )

@app.route('/manager_low_product_delete_azka/<int:id_azka>', methods=['GET'])
def manager_low_product_delete_azka(id_azka):
    if 'user_id_azka' not in session:
        flash("Silakan login dulu!", "warning")
        return redirect(url_for('login_azka'))

    conn = get_db_connection_azka()
    cursor = conn.cursor()

    cursor.execute("SELECT nama_azka FROM tbl_product_azka WHERE id_azka=%s", (id_azka,))
    row = cursor.fetchone()
    nama_barang = row[0] if row else "Tidak diketahui"

    cursor.execute("DELETE FROM tbl_product_azka WHERE id_azka=%s", (id_azka,))
    conn.commit()

    conn.close()

    insert_log_azka(session['user_id_azka'], "Delete", f"Hapus barang: {nama_barang}")

    flash("Barang berhasil dihapus!", "danger")
    return redirect(url_for('manager_stock_monitor_azka'))

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

    if scan_type not in ['IN', 'OUT'] or not warehouse_id:
        return "Invalid data", 400

    conn = get_db_connection_azka()
    cursor = conn.cursor(dictionary=True)

    # ===============================
    # 1️⃣ CEK SHIPMENT AKTIF KURIR
    # ===============================
    cursor.execute("""
        SELECT * FROM tbl_shipment_azka
        WHERE courier_id_azka=%s
          AND status_azka NOT IN ('DELIVERED')
        LIMIT 1
    """, (courier_id,))
    shipment = cursor.fetchone()

    # ===============================
    # 2️⃣ AUTO AMBIL SHIPMENT (JIKA BELUM ADA)
    # ===============================
    if not shipment:
        cursor.execute("""
            SELECT * FROM tbl_shipment_azka
            WHERE courier_id_azka IS NULL
              AND status_azka = 'CREATED'
              AND warehouse_id_azka = %s
            ORDER BY created_at_azka ASC
            LIMIT 1
        """, (warehouse_id,))
        shipment = cursor.fetchone()

        if not shipment:
            conn.close()
            return "Tidak ada shipment di gudang ini", 404

       # assign ke kurir + pickup
        cursor.execute("""
            UPDATE tbl_shipment_azka
            SET courier_id_azka=%s,
                status_azka='PICKED_UP'
            WHERE id_azka=%s
        """, (courier_id, shipment['id_azka']))
        conn.commit()

    # 📍 Ambil koordinat gudang
    cursor.execute("""
        SELECT latitude_azka, longitude_azka
        FROM tbl_warehouses_azka
        WHERE id_azka = %s
    """, (warehouse_id,))
    wh = cursor.fetchone()

    if not wh:
        conn.close()
        return "Gudang tidak ditemukan", 404

    lat = wh['latitude_azka']
    lng = wh['longitude_azka']

    # ===============================
    # 3️⃣ FLOW STATUS VALID
    # ===============================
    status = shipment['status_azka']
    new_status = None

    if status == 'CREATED' and scan_type == 'IN':
        new_status = 'PICKED_UP'
    # keluar gudang
    elif status == 'PICKED_UP' and scan_type == 'OUT':
        new_status = 'IN_TRANSIT'

    elif status == 'IN_TRANSIT' and scan_type == 'IN':
        new_status = 'ARRIVED_AT_DEST_HUB'

    elif status == 'ARRIVED_AT_DEST_HUB' and scan_type == 'OUT':
        new_status = 'OUT_FOR_DELIVERY'

    elif status == 'OUT_FOR_DELIVERY' and scan_type == 'IN':
        new_status = 'DELIVERED'

        # lepas shipment dari kurir
        cursor.execute("""
            UPDATE tbl_shipment_azka
            SET courier_id_azka=NULL
            WHERE id_azka=%s
        """, (shipment['id_azka'],))

    else:
        conn.close()
        return f"Scan tidak valid ({status} + {scan_type})", 400

    # ===============================
    # 4️⃣ UPDATE SHIPMENT
    # ===============================
    cursor.execute("""
        UPDATE tbl_shipment_azka
        SET status_azka=%s,
            warehouse_id_azka=%s
        WHERE id_azka=%s
    """, (new_status, warehouse_id, shipment['id_azka']))

    # ===============================
    # 5️⃣ SIMPAN LOG
    # ===============================
    cursor.execute("""
        INSERT INTO tbl_courier_scans_azka
        (courier_id_azka, warehouse_id_azka, scan_type_azka,
        latitude_azka, longitude_azka, scan_time_azka)
        VALUES (%s,%s,%s,%s,%s,NOW())
    """, (courier_id, warehouse_id, scan_type, lat, lng))

    cursor.execute("""
        INSERT INTO tbl_activity_logs_azka
        (user_id_azka, actions_azka, created_at_azka)
        VALUES (%s,%s,NOW())
    """, (
        courier_id,
        f"Scan {scan_type} | {shipment['tracking_number_azka']} → {new_status}"
    ))

    conn.commit()
    conn.close()
    return "OK"

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
