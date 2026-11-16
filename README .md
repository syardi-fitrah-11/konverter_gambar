# Image Converter Pro

Aplikasi desktop berbasis Python untuk mengubah ukuran resolusi dan mengonversi format banyak gambar sekaligus (*batch processing*) dengan antarmuka modern (*Dark Mode*).

## Fitur Utama

* **Drag & Drop & Multi-File Picker:** Seret dan lepas banyak foto sekaligus ke jendela aplikasi atau pilih melalui manajer file.
* **Pilihan Ukuran Resolusi Lengkap:** Tersedia daftar ukuran siap pakai mulai dari ukuran asli hingga resolusi 4K tanpa mengubah proporsi rasio gambar.
* **Mode Anti-Pecah (*Smart Sharpen*):** Mempertajam tepi piksel secara otomatis menggunakan filter *Unsharp Mask* saat gambar diperbesar melebihi dimensi aslinya.
* **Kompresi Ukuran File Cerdas:** Menghapus metadata tersembunyi (EXIF), menerapkan kuantisasi warna adaptif, serta mendukung format modern **WebP**, **JPG**, dan **PNG** untuk memangkas ukuran file secara signifikan.

---

## Daftar Ukuran Resolusi yang Tersedia

Aplikasi ini menyediakan pilihan lebar gambar berbasis daftar (*dropdown list*) yang otomatis menyesuaikan tinggi secara proporsional:

| Pilihan Ukuran | Lebar Target | Kegunaan Umum |
| :--- | :--- | :--- |
| **Asli (Tidak Diubah)** | Sesuai file sumber | Hanya mengompres ukuran file atau mengubah format tanpa mengubah dimensi |
| **480 px (Mobile)** | `480 px` | Thumbnail ringan, ikon web, atau tampilan layar ponsel |
| **720 px (SD)** | `720 px` | Unggahan media sosial standar dan pengiriman pesan cepat |
| **1080 px (Full HD)** | `1080 px` | Konten Instagram, banner web, dan presentasi standar |
| **1280 px (HD Web)** | `1280 px` | Gambar artikel blog, sampul video HD, dan aset website |
| **1920 px (Full HD+)** | `1920 px` | Wallpaper layar penuh, portofolio digital, dan layar monitor standar |
| **2560 px (2K QHD)** | `2560 px` | Layar resolusi tinggi dan kebutuhan cetak ukuran sedang |
| **3840 px (4K UHD)** | `3840 px` | Layar Ultra HD, desain beresolusi tinggi, dan pencetakan besar |

---

## Cara Instalasi & Pemakaian

### 1. Unduh Proyek
Kloning repositori atau unduh sebagai ZIP lalu ekstrak:
```bash
git clone https://github.com/USERNAME_KAMU/image-converter-pro.git
cd image-converter-pro
```

### 2. Pengguna Windows (Instalasi Otomatis 1-Klik)
1. Pastikan **Python** sudah terinstal di Windows (centang *"Add Python to PATH"* saat instalasi Python).
2. Klik ganda pada file **`setup_windows.bat`**.
3. Skrip akan otomatis mengunduh seluruh library yang dibutuhkan (`Pillow`, `customtkinter`, `tkinterdnd2`) dan membuatkan ikon pintasan **`Image Converter Pro`** langsung di **Desktop**.

### 3. Pengguna Linux (Menjalankan dengan `python3`)
1. Pastikan paket sistem `python3-tk` dan `pip` sudah terpasang (contoh untuk Ubuntu/Debian):
   ```bash
   sudo apt update && sudo apt install python3-tk python3-pip -y
   ```
2. Instal library yang dibutuhkan:
   ```bash
   python3 -m pip install Pillow customtkinter tkinterdnd2 --break-system-packages
   ```
3. Jalankan aplikasi langsung dengan `python3`:
   ```bash
   python3 app_konverter-v2.py
   ```

---

## Cara Penggunaan Aplikasi

1. **Masukkan Gambar:** Seret dan lepas foto ke kotak biru atau klik kotak tersebut untuk memilih file dari folder.
2. **Pilih Ukuran & Format:** Tentukan target lebar dari daftar ukuran yang tersedia, lalu pilih format tujuan (`webp`, `jpg`, atau `png`).
3. **Atur Kualitas & Ketajaman:** Geser tingkat kualitas kompresi sesuai kebutuhan dan pastikan saklar **Mode Anti-Pecah** aktif jika memperbesar resolusi gambar.
4. **Konversi:** Klik **Mulai Konversi**. Semua hasil otomatis tersimpan di dalam folder `hasil_konversi`.
