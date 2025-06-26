# Smart-Sprite-Splitter---Auto-Detect-Custom-Count
Smart Sprite Splitter - Auto Detect &amp; Custom Count 100% Work No Root 🤫🧏‍♂️


Before you using this pls install
***pip install pillow***

# 🎯 Smart Sprite Splitter

Tool untuk memisahkan sprite sheet menjadi gambar individual dengan dukungan jumlah sprite yang berbeda-beda per file. Cocok untuk memproses ratusan hingga ribuan file sprite sheet sekaligus.

## ✨ Fitur Utama

- 🤖 **Auto-Detection**: Otomatis mendeteksi jumlah sprite dalam gambar
- 📝 **Manual Configuration**: Input jumlah sprite per file secara manual
- 🗂️ **Batch Processing**: Proses ratusan/ribuan file sekaligus
- ⚡ **Multi-Threading**: Processing paralel untuk kecepatan maksimal
- 📂 **Folder Structure**: Pertahankan struktur folder atau flatten ke root
- 🔄 **Recursive Search**: Cari file di semua subfolder
- 📊 **Progress Tracking**: Monitor progress real-time dengan ETA
- ⚙️ **Flexible Config**: JSON config file untuk setup yang kompleks

## 📋 Requirements

```bash
pip install pillow numpy
```

## 🚀 Quick Start

### 1. Setup Folder Structure
```
project/
├── input/              # Taruh sprite sheets di sini
│   ├── character1.png  # 3 sprites
│   ├── character2.png  # 8 sprites
│   └── enemy1.png      # 6 sprites
├── output/             # Hasil akan muncul di sini (auto-created)
└── sprite_splitter.py  # Script utama
```

### 2. Jalankan Script
```bash
python sprite_splitter.py
```

### 3. Pilih Mode
```
PILIH MODE:
1. Auto-detect sprite count (cepat)
2. Manual input per file (akurat)
3. Load dari config file
4. Buat config file saja

Pilih (1/2/3/4): 1
```

## 📖 Mode Operasi

### Mode 1: Auto-Detect (Recommended untuk Start)
- Script otomatis mendeteksi jumlah sprite
- Paling cepat untuk volume besar
- Akurasi ~80-90% tergantung jenis sprite

**Metode Deteksi:**
- **Transparency Detection**: Mencari kolom transparan sebagai pemisah
- **Color Change Detection**: Deteksi perubahan warna drastis
- **Aspect Ratio**: Estimasi berdasarkan proporsi gambar

### Mode 2: Manual Input
- Input jumlah sprite untuk setiap file
- Paling akurat tapi memakan waktu
- Cocok untuk file sedikit atau yang penting

**Contoh:**
```
warrior.png [saran: 8]: 3        # Input 3
mage.png [saran: 6]: 8          # Input 8
goblin.png [saran: 4]: 6        # Input 6
boss.png [saran: 2]: [Enter]    # Pakai saran (2)
```

### Mode 3: Config File
- Load konfigurasi dari file JSON
- Ideal untuk setup yang sudah final
- Bisa diedit manual untuk fine-tuning

### Mode 4: Generate Config Only
- Buat file konfigurasi tanpa memproses
- Edit manual untuk akurasi maksimal
- Jalankan ulang dengan Mode 3

## 📁 Input & Output

### Input Structure (Flexible)
```
input/
├── characters/
│   ├── heroes/
│   │   ├── warrior.png     # 3 sprites horizontal
│   │   └── mage.png        # 8 sprites horizontal
│   └── enemies/
│       ├── goblin.png      # 6 sprites horizontal
│       └── orc.png         # 4 sprites horizontal
├── items/
│   ├── weapons.png         # 5 sprites horizontal
│   └── armor.png           # 7 sprites horizontal
└── single_character.png    # 12 sprites horizontal
```

### Output Structure
```
output/
├── characters/
│   ├── heroes/
│   │   ├── warrior/
│   │   │   ├── sprite_01.png
│   │   │   ├── sprite_02.png
│   │   │   └── sprite_03.png
│   │   └── mage/
│   │       ├── sprite_01.png
│   │       ├── sprite_02.png
│   │       ├── ...
│   │       └── sprite_08.png
│   └── enemies/
│       ├── goblin/
│       │   ├── sprite_01.png
│       │   ├── ...
│       │   └── sprite_06.png
│       └── orc/
│           ├── sprite_01.png
│           ├── ...
│           └── sprite_04.png
├── items/
└── single_character/
    ├── sprite_01.png
    ├── ...
    └── sprite_12.png
```

## ⚙️ Configuration File Format

### sprite_config.json
```json
{
  "characters/heroes/warrior.png": {
    "sprite_count": 3,
    "auto_detected": false,
    "file_size": 245760
  },
  "characters/heroes/mage.png": {
    "sprite_count": 8,
    "auto_detected": false,
    "file_size": 512000
  },
  "characters/enemies/goblin.png": {
    "sprite_count": 6,
    "auto_detected": true,
    "file_size": 128000
  }
}
```

**Field Explanation:**
- `sprite_count`: Jumlah sprite dalam gambar
- `auto_detected`: Apakah hasil auto-detection atau manual
- `file_size`: Ukuran file (untuk referensi)

## 🎯 Use Cases

### Scenario 1: Game Developer (810 Sprite Sheets)
```bash
# Step 1: Auto-detect semua
python sprite_splitter.py
# Pilih mode 1, biarkan auto-detect

# Step 2: Review hasil auto-detection
# Edit sprite_config.json untuk yang salah

# Step 3: Re-process dengan config yang sudah diedit
python sprite_splitter.py
# Pilih mode 3, load dari config
```

### Scenario 2: Mix Manual & Auto
```bash
# Step 1: Generate config
python sprite_splitter.py
# Pilih mode 4

# Step 2: Edit config file manual
# Sesuaikan sprite_count untuk file-file penting

# Step 3: Process
python sprite_splitter.py
# Pilih mode 3
```

### Scenario 3: Small Batch, High Accuracy
```bash
python sprite_splitter.py
# Pilih mode 2 (manual input)
# Input jumlah sprite per file
```

## 📊 Performance

### Benchmarks
- **Single Thread**: ~2-3 files/detik
- **8 Threads**: ~15-20 files/detik
- **810 Files**: ~5-10 menit (tergantung ukuran)

### Memory Usage
- **Auto-detect**: ~50-100MB RAM
- **Large files** (>10MB): Temporary spike saat processing

### Supported Formats
- ✅ PNG (recommended)
- ✅ JPG/JPEG
- ✅ BMP
- ✅ TIFF
- ⚠️ GIF (limited support)

## 🛠️ Advanced Usage

### Custom Thread Count
Edit di script:
```python
max_workers = 8  # Sesuaikan dengan CPU cores
```

### Custom Output Format
Edit di script:
```python
output_path = os.path.join(output_dir, f"sprite_{i+1:02d}.jpg")  # JPG output
```

### Filter Files by Name
```python
# Hanya proses file yang mengandung keyword tertentu
keywords = ["character", "sprite", "hero"]
filtered_files = [f for f in all_files 
                  if any(k in os.path.basename(f).lower() for k in keywords)]
```

## 🐛 Troubleshooting

### Common Issues

**"Auto-detect gagal"**
- Coba mode manual untuk file tersebut
- Pastikan sprite tersusun horizontal
- Check apakah ada transparency atau color separation

**"Memory Error"**
- Kurangi `max_workers`
- Process file besar satu per satu
- Resize gambar sebelum diproses

**"File tidak ditemukan"**
- Check path folder input
- Pastikan ekstensi file didukung
- Check permission read/write

**"Hasil sprite terpotong"**
- Sprite mungkin tidak aligned perfect
- Coba manual input untuk file tersebut
- Edit `sprite_width` calculation di script

### Debug Mode
Tambahkan di script untuk debugging:
```python
print(f"Debug: width={width}, sprite_count={sprite_count}, sprite_width={sprite_width}")
```

## 🔧 Customization

### Custom Auto-Detection
Modify function `auto_detect_sprites()` untuk metode detection khusus:

```python
def auto_detect_sprites(img_path, method="custom"):
    # Implementasi custom detection logic
    pass
```

### Custom Naming Convention
```python
# Ganti format nama output
output_path = os.path.join(output_dir, f"{file_name}_{i+1:03d}.png")
# Hasil: warrior_001.png, warrior_002.png, dst.
```

## 📝 Tips & Best Practices

### Preparation
1. **Backup** file original sebelum processing
2. **Organize** folder structure yang konsisten
3. **Test** dengan sample kecil dulu
4. **Check** ukuran dan format file

### Optimization
1. **Use SSD** untuk speed maksimal
2. **Close other apps** saat processing volume besar
3. **Monitor RAM usage** untuk file besar
4. **Use PNG** untuk transparency support

### Quality Control
1. **Spot check** beberapa hasil random
2. **Verify** sprite count untuk file penting
3. **Check** alignment dan cropping
4. **Test** hasil sprite di aplikasi target

## 📄 License

MIT License - Feel free to modify and distribute

## 🤝 Contributing

Issues dan pull requests welcome! Terutama untuk:
- Algoritma auto-detection yang lebih baik
- Support format file baru
- Performance optimization
- UI improvements

## 📞 Support

Jika ada masalah atau pertanyaan:
1. Check troubleshooting section
2. Review config file format
3. Test dengan sample kecil
4. Share error message dan sample file untuk debugging

---

**Happy Sprite Splitting!** 🎮✨