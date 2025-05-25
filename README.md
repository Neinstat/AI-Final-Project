# AI-Final-Project

# Face Similarity Checker

Aplikasi untuk memeriksa kemiripan wajah antara dua gambar menggunakan **DeepFace**. Aplikasi ini memungkinkan pengguna untuk meng-upload dua gambar wajah dan mendapatkan persentase kemiripan di antara keduanya. Aplikasi ini dibangun dengan menggunakan **Vue.js** di frontend dan **Flask** di backend.

## Fitur

- Upload dua gambar wajah secara otomatis.
- Menampilkan gambar yang telah di-upload.
- Menghitung persentase kemiripan wajah antara dua gambar menggunakan DeepFace.
- Menampilkan hasil kemiripan dalam bentuk persentase.
- Menambahkan spinner loading untuk menunjukkan proses upload dan prediksi.

## Prasyarat

Sebelum menjalankan aplikasi, pastikan Anda telah menginstal **Python**, **Node.js**, dan **npm** di sistem Anda.

## Langkah-langkah Instalasi dan Penggunaan

### 1. **Instalasi Backend (Flask)**
```
cd backend
```

```
pip install flask flask-cors deepface werkzeug
```

### 2. **Instalasi Frontend (Vue)**
```
cd frontend
```

```
npm install
```

### 3. **Jalankan Aplikasi**
```
cd backend
python app.py
```

```
cd frontend
npm run serve
```
