# Smart Sprite Splitter

**Smart Sprite Splitter** adalah tool Python untuk memecah (split) gambar sprite sheet menjadi beberapa file gambar kecil secara otomatis maupun manual, dengan deteksi jumlah sprite per gambar.

## Fitur

- **Auto-detect jumlah sprite** pada setiap gambar (berbasis transparansi, perubahan warna, atau fallback aspect ratio).
- **Input manual** jumlah sprite per file jika ingin lebih akurat.
- **Batch processing** dengan multi-threading (cepat untuk banyak file).
- **Konfigurasi per file** (bisa edit jumlah sprite di file JSON).
- **Bisa menggunakan folder input/output dari mana saja** (isi path folder sesuai keinginan, tidak harus di dalam folder project).

## Cara Pakai

### 1. Instalasi Dependensi

Pastikan Python 3 sudah terpasang.  
Install library yang dibutuhkan:

```bash
pip install pillow numpy
```

### 2. Jalankan Program

```bash
python SmartSprite.py
```

### 3. Pilih Mode

Saat dijalankan, pilih mode sesuai kebutuhan:

1. **Auto-detect sprite count (cepat)**  
   Deteksi otomatis jumlah sprite pada setiap gambar.

2. **Manual input per file (akurat)**  
   Input jumlah sprite untuk setiap file secara manual.

3. **Load dari config file**  
   Gunakan konfigurasi jumlah sprite dari file JSON yang sudah ada.

4. **Buat config file saja**  
   Hanya membuat file konfigurasi jumlah sprite (tanpa split gambar).

### 4. Input Folder

- Saat diminta "Input folder" dan "Output folder", **isi dengan path folder yang kamu mau**.
- Path boleh absolut (misal `D:\Asset Negara\input_sprites`) atau relatif (`input`).
- Tidak perlu membuat folder khusus di dalam project, program akan otomatis membuat folder jika belum ada.

**Contoh:**
```
Input folder: D:\Asset Negara\input_sprites
Output folder: D:\Asset Negara\output_sprites
```

### 5. Hasil

- Gambar hasil split akan disimpan di folder output yang kamu tentukan.
- File konfigurasi (JSON) akan tersimpan di folder input atau sesuai path yang kamu pilih.

## Catatan

- Jika ingin mengedit jumlah sprite per gambar, edit file konfigurasi JSON yang dihasilkan.
- Untuk folder dengan spasi, cukup copy-paste path dari Windows Explorer (tidak perlu tanda kutip).
- Shortcut Windows (.lnk) tidak didukung, gunakan path asli folder.

## Lisensi

MIT License

---

**By:** [MohNahrowiSetiawan](https://github.com/Mohnahrowisetiawan217)