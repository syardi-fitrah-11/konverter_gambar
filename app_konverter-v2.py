import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageFilter

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TkModernDnD(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class AplikasiKonverterModern:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Studio — Smart Upscale & Compressor")
        self.root.geometry("520x610")
        self.root.resizable(False, False)

        self.daftar_file = []
        self.folder_hasil = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hasil_konversi")
        os.makedirs(self.folder_hasil, exist_ok=True)

        self.buat_tampilan()

    def buat_tampilan(self):
        header_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        ctk.CTkLabel(
            header_frame, text="Image Converter Pro", 
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_frame, text="Perbesar tanpa pecah & perkecil ukuran file secara cerdas", 
            font=ctk.CTkFont(size=12), text_color="#94a3b8"
        ).pack(anchor="w")

        self.card_drop = ctk.CTkFrame(
            self.root, height=135, corner_radius=15, 
            fg_color="#1e293b", border_width=2, border_color="#3b82f6"
        )
        self.card_drop.pack(fill="x", padx=25, pady=10)
        self.card_drop.pack_propagate(False)

        self.lbl_drop_icon = ctk.CTkLabel(
            self.card_drop, text="📁", font=ctk.CTkFont(size=32)
        )
        self.lbl_drop_icon.pack(pady=(20, 0))

        self.lbl_drop_teks = ctk.CTkLabel(
            self.card_drop, 
            text="Seret & Lepas Gambar di Sini\natau klik area ini untuk memilih file",
            font=ctk.CTkFont(size=13, weight="bold"), text_color="#e2e8f0"
        )
        self.lbl_drop_teks.pack(pady=(5, 0))

        for widget in (self.card_drop, self.lbl_drop_icon, self.lbl_drop_teks):
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind('<<Drop>>', self.saat_file_dilepas)
            widget.bind("<Button-1>", lambda e: self.pilih_file_manual())

        self.lbl_status = ctk.CTkLabel(
            self.root, text="Belum ada gambar yang dipilih", 
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#64748b"
        )
        self.lbl_status.pack(pady=(2, 8))

        card_opsi = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#1e293b")
        card_opsi.pack(fill="x", padx=25, pady=5)

        ctk.CTkLabel(card_opsi, text="Pilih Ukuran Lebar", font=ctk.CTkFont(size=13)).grid(
            row=0, column=0, sticky="w", padx=20, pady=(15, 8)
        )
        self.pilihan_ukuran = ctk.CTkOptionMenu(
            card_opsi, 
            values=[
                "Asli (Tidak Diubah)",
                "480 px (Mobile)",
                "720 px (SD)",
                "1080 px (Full HD)",
                "1280 px (HD Web)",
                "1920 px (Full HD+)",
                "2560 px (2K QHD)",
                "3840 px (4K UHD)"
            ],
            width=185
        )
        self.pilihan_ukuran.set("1280 px (HD Web)")
        self.pilihan_ukuran.grid(row=0, column=1, sticky="e", padx=20, pady=(15, 8))

        ctk.CTkLabel(card_opsi, text="Format Tujuan", font=ctk.CTkFont(size=13)).grid(
            row=1, column=0, sticky="w", padx=20, pady=8
        )
        self.pilihan_format = ctk.CTkSegmentedButton(
            card_opsi, values=["webp", "jpg", "png"], width=185
        )
        self.pilihan_format.set("webp")
        self.pilihan_format.grid(row=1, column=1, sticky="e", padx=20, pady=8)

        self.lbl_kualitas = ctk.CTkLabel(card_opsi, text="Kualitas Kompresi: 75%", font=ctk.CTkFont(size=13))
        self.lbl_kualitas.grid(row=2, column=0, sticky="w", padx=20, pady=8)
        
        self.slider_kualitas = ctk.CTkSlider(
            card_opsi, from_=10, to=100, number_of_steps=90, width=185,
            command=self.update_label_kualitas
        )
        self.slider_kualitas.set(75)
        self.slider_kualitas.grid(row=2, column=1, sticky="e", padx=20, pady=8)

        self.switch_sharpen = ctk.CTkSwitch(
            card_opsi, text="Mode Anti-Pecah (Smart Sharpen saat diperbesar)",
            font=ctk.CTkFont(size=12)
        )
        self.switch_sharpen.select()
        self.switch_sharpen.grid(row=3, column=0, columnspan=2, sticky="w", padx=20, pady=(8, 15))

        card_opsi.grid_columnconfigure(1, weight=1)

        frame_tombol = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_tombol.pack(fill="x", padx=25, pady=(18, 8))

        self.btn_proses = ctk.CTkButton(
            frame_tombol, text="Mulai Konversi", height=42, corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.proses_semua_gambar
        )
        self.btn_proses.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self.btn_reset = ctk.CTkButton(
            frame_tombol, text="Reset", width=90, height=42, corner_radius=10,
            fg_color="#334155", hover_color="#475569",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.reset_daftar
        )
        self.btn_reset.pack(side="right")

        btn_buka_folder = ctk.CTkButton(
            self.root, text="📂 Buka Folder Hasil Konversi", height=32,
            fg_color="transparent", border_width=1, border_color="#334155",
            text_color="#94a3b8", hover_color="#1e293b",
            command=self.buka_folder_hasil
        )
        btn_buka_folder.pack(fill="x", padx=25, pady=(5, 15))

    def update_label_kualitas(self, value):
        self.lbl_kualitas.configure(text=f"Kualitas Kompresi: {int(value)}%")

    def saat_file_dilepas(self, event):
        raw_files = self.root.tk.splitlist(event.data)
        clean_files = [f[7:] if f.startswith("file://") else f for f in raw_files]
        self.tambah_ke_daftar(clean_files)

    def pilih_file_manual(self):
        files = filedialog.askopenfilenames(
            title="Pilih Gambar",
            initialdir=os.path.expanduser("~/Downloads"),
            filetypes=[("File Gambar", "*.png *.jpg *.jpeg *.webp *.bmp")]
        )
        if files:
            self.tambah_ke_daftar(files)

    def tambah_ke_daftar(self, files):
        ekstensi_valid = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
        for f in files:
            if f.lower().endswith(ekstensi_valid) and f not in self.daftar_file:
                self.daftar_file.append(f)
        
        if self.daftar_file:
            total_kb = sum(os.path.getsize(f) for f in self.daftar_file) / 1024
            self.lbl_status.configure(
                text=f"✓ {len(self.daftar_file)} gambar dipilih (Total: {total_kb:.1f} KB)", 
                text_color="#34d399"
            )
            self.card_drop.configure(border_color="#34d399")

    def reset_daftar(self):
        self.daftar_file.clear()
        self.lbl_status.configure(text="Belum ada gambar yang dipilih", text_color="#64748b")
        self.card_drop.configure(border_color="#3b82f6")

    def buka_folder_hasil(self):
        subprocess.Popen(["xdg-open", self.folder_hasil])

    def proses_semua_gambar(self):
        if not self.daftar_file:
            messagebox.showwarning("Peringatan", "Seret atau pilih gambar terlebih dahulu!")
            return

        pilihan_teks = self.pilihan_ukuran.get()
        kualitas = int(self.slider_kualitas.get())
        format_tujuan = self.pilihan_format.get()

        berhasil = 0
        total_awal = 0
        total_akhir = 0

        for path_asal in self.daftar_file:
            try:
                total_awal += os.path.getsize(path_asal)
                with Image.open(path_asal) as img:
                    lebar_asli, tinggi_asli = img.size

                    if pilihan_teks.startswith("Asli"):
                        lebar_baru, tinggi_baru = lebar_asli, tinggi_asli
                    else:
                        lebar_baru = int(pilihan_teks.split()[0])
                        rasio = lebar_baru / float(lebar_asli)
                        tinggi_baru = int(tinggi_asli * rasio)

                    if lebar_baru != lebar_asli:
                        img_hasil = img.resize((lebar_baru, tinggi_baru), Image.Resampling.LANCZOS)
                    else:
                        img_hasil = img.copy()

                    if lebar_baru > lebar_asli and self.switch_sharpen.get() == 1:
                        img_hasil = img_hasil.filter(
                            ImageFilter.UnsharpMask(radius=1.5, percent=130, threshold=3)
                        )

                    data_bersih = list(img_hasil.getdata())
                    img_bersih = Image.new(img_hasil.mode, img_hasil.size)
                    img_bersih.putdata(data_bersih)

                    nama_asli = os.path.splitext(os.path.basename(path_asal))[0]
                    nama_baru = f"{nama_asli}_opt.{format_tujuan}"
                    path_tujuan = os.path.join(self.folder_hasil, nama_baru)

                    if format_tujuan in ['jpg', 'jpeg']:
                        if img_bersih.mode in ('RGBA', 'P'):
                            img_bersih = img_bersih.convert('RGB')
                        img_bersih.save(
                            path_tujuan, format='JPEG', quality=kualitas, 
                            optimize=True, progressive=True
                        )
                    elif format_tujuan == 'webp':
                        img_bersih.save(
                            path_tujuan, format='WEBP', quality=kualitas, method=6
                        )
                    elif format_tujuan == 'png':
                        if img_bersih.mode == 'RGBA':
                            img_bersih = img_bersih.quantize(colors=256, method=Image.Quantize.FASTOCTREE)
                        else:
                            img_bersih = img_bersih.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)
                        img_bersih.save(path_tujuan, format='PNG', optimize=True)

                    total_akhir += os.path.getsize(path_tujuan)
                    berhasil += 1
            except Exception as e:
                print(f"Gagal memproses {path_asal}: {e}")

        awal_kb = total_awal / 1024
        akhir_kb = total_akhir / 1024
        selisih_persen = ((total_awal - total_akhir) / total_awal * 100) if total_awal > 0 else 0

        pesan_ukuran = (
            f"Ukuran awal: {awal_kb:.1f} KB\n"
            f"Ukuran baru: {akhir_kb:.1f} KB\n"
        )
        if selisih_persen > 0:
            pesan_ukuran += f"Hemat ruang: {selisih_persen:.1f}% lebih ringan!"
        else:
            pesan_ukuran += "Resolusi diperbesar dengan ketajaman optimal."

        messagebox.showinfo("Konversi Selesai", f"Berhasil memproses {berhasil} gambar!\n\n{pesan_ukuran}")
        self.reset_daftar()

if __name__ == "__main__":
    root = TkModernDnD()
    app = AplikasiKonverterModern(root)
    root.mainloop()
