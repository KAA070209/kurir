# 🚚 Logistics – Sistem Manajemen Logistik Berbasis Web

Aplikasi **Logistics** adalah sistem manajemen logistik berbasis **Flask + MySQL** yang dirancang untuk mengelola proses pengiriman barang secara terstruktur, mulai dari pembuatan shipment, assign driver, sortir gudang, hingga pengiriman ke kurir.

Sistem ini mendukung multi-role user seperti **Admin, Gudang, Kurir, dan Driver**, lengkap dengan QR Code system dan tracking berbasis koordinat.

---

# 🏗️ Arsitektur Sistem

* Backend: Python (Flask)
* Database: MySQL
* Frontend: HTML, Bootstrap
* QR Code: Python `qrcode`
* Geocoding: OpenStreetMap (Nominatim API)
* Map Routing: Perhitungan jarak Haversine
* Session Management: Flask Session
* Security: Password Hashing (Werkzeug)

---

# 👥 Role & Hak Akses

| Role      | Akses                     |
| --------- | ------------------------- |
| 👑 Admin  | Full akses sistem         |
| 🏢 Gudang | Sortir & distribusi paket |
| 🚚 Driver | Antar antar-hub           |
| 📦 Kurir  | Antar ke penerima         |

---

# 🚀 Fitur Lengkap Sistem

## 🔐 1. Authentication & Security

* Login multi-role
* Session protection
* Password hashing (PBKDF2)
* Role-based access control
* Auto update last activity
* Activity logs (Login / Logout / Action)

---

## 👑 2. Admin Features

### 📊 Dashboard Monitoring

* Total user
* Total gudang
* Total shipment
* Total barang
* Status shipment real-time
* Posisi kurir & driver (IN/OUT gudang)
* Log aktivitas terbaru

### 👤 Manajemen User

* Tambah user
* Edit user
* Reset password
* Hapus user (dengan validasi relasi)
* Status online detection
* Assign wilayah khusus kurir

### 🏢 Manajemen Gudang

* Tambah gudang (auto geocoding)
* Edit gudang
* Hapus gudang (dengan validasi relasi)
* Generate QR gudang otomatis
* Simpan koordinat latitude & longitude

### 📦 Manajemen Shipment

* Buat shipment baru
* Generate tracking number otomatis
* Generate QR Paket otomatis
* Hitung rute origin → hub terdekat → destination
* Assign driver via scan QR
* Delete shipment dengan validasi status
* Lock transaction (FOR UPDATE)

### 📈 Laporan & Analitik

* Status shipment
* Shipment per gudang
* Aktivitas kurir
* Aktivitas driver
* Shipment per kota
* Trend delivered per bulan

---

## 🏢 3. Gudang Features

* Dashboard sortir berdasarkan kota
* Scan paket masuk sortir
* Scan kurir untuk ready delivery
* Validasi wilayah kurir
* Validasi status paket
* Monitoring shipment dalam perjalanan
* Manajemen lokasi gudang

---

## 🚚 4. Driver Features

* QR Driver
* Scan IN / OUT gudang
* Tracking status antar pulau / antar kota
* Validasi tidak bisa aktif di 2 gudang berbeda
* Log aktivitas otomatis

---

## 📦 5. Kurir Features

* QR Kurir pribadi
* Scan IN / OUT gudang
* Ambil paket sesuai wilayah
* Validasi wilayah pengiriman
* Dashboard status terakhir
* Log aktivitas penyerahan paket

---

## 🌍 6. Sistem Geolocation & Routing

* Geocoding alamat otomatis
* Simpan latitude & longitude
* Hitung jarak menggunakan rumus Haversine
* Tentukan hub terdekat otomatis
* Simulasi posisi truck

---

## 🔄 7. Status Flow Shipment

```
CREATED
↓
DRIVER_ASSIGNED
↓
PICKUP
↓
ARRIVED_AT_ORIGIN_HUB
↓
IN_TRANSIT
↓
TRANSIT_HUB
↓
SORTING
↓
READY_FOR_DELIVERY
↓
DELIVERED
```

Sistem memiliki validasi ketat agar status tidak bisa lompat.

---

## 📁 Struktur Project

```
aplikasi-logistik/
│
├── app.py
├── templates/
├── static/
│   ├── qr_paket/
│   ├── qr_kurir/
│   └── qr_gudang_azka/
└── .env
└── app.py
└── config.py
├── README.md
└── requirements.txt
└── wsgi.py
```

---

# ⚙️ Instalasi

### 1️⃣ Clone Repository

```bash
git clone https://github.com/KAA070209/aplikasi-logistik.git
cd aplikasi-logistik
```

### 2️⃣ Buat Virtual Environment

```bash
python -3 -m venv .venv
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### 3️⃣ Install Dependency

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variable

Set environment variable:

```
set FLASK_APP=app.py
set FLASK_ENV=development
```

### 5️⃣ Jalankan Aplikasi

```bash
flask --debug run
```

Akses di:

```
http://127.0.0.1:5000
```

---

# 🛡️ Keamanan Sistem

* Transaction-safe database operation
* Row locking (SELECT ... FOR UPDATE)
* QR validation strict parsing
* Role-based route protection
* Input validation
* Prevention duplicate scan
* Prevent delete processed shipment

---

# 📌 Keunggulan Sistem

✅ Real multi-role system
✅ QR-based logistics workflow
✅ Auto geocoding address
✅ Hub nearest calculation
✅ Warehouse region validation
✅ Strict shipment state machine
✅ Monitoring & reporting dashboard
✅ Full activity audit log

---

# 📌 Potensi Pengembangan

* Real-time GPS tracking
* Push notification
* REST API external integration
* Export laporan PDF / Excel
* Multi-branch logistic network
* SLA monitoring

---

# 👨‍💻 Developer

Developed by: **KAA070209**

---

