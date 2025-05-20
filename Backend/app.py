import os
from flask import Flask, request, jsonify
from deepface import DeepFace
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)

# Aktifkan CORS untuk memungkinkan akses dari frontend Vue.js
CORS(app)

# Konfigurasi folder untuk menyimpan gambar
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'HEIC'}

# Fungsi untuk mengecek apakah file yang di-upload valid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route utama untuk halaman pertama
@app.route('/')
def index():
    return "Face Similarity API is running!"

# Route untuk meng-upload gambar pertama
@app.route('/upload_image1', methods=['POST'])
def upload_image1():
    # Periksa apakah ada file yang di-upload dengan key 'image1'
    if 'image1' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file1 = request.files['image1']
    
    # Periksa apakah file yang dipilih kosong
    if file1.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Periksa apakah ekstensi file valid
    if file1 and allowed_file(file1.filename):
        filename1 = secure_filename(file1.filename)
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
        file1.save(filepath1)  # Simpan file di server
        return jsonify({"message": "Image 1 uploaded successfully"}), 200
    
    return jsonify({"error": "File format not allowed"}), 400

# Route untuk meng-upload gambar kedua
@app.route('/upload_image2', methods=['POST'])
def upload_image2():
    # Periksa apakah ada file yang di-upload dengan key 'image2'
    if 'image2' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file2 = request.files['image2']
    
    # Periksa apakah file yang dipilih kosong
    if file2.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Periksa apakah ekstensi file valid
    if file2 and allowed_file(file2.filename):
        filename2 = secure_filename(file2.filename)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg')
        file2.save(filepath2)  # Simpan file di server
        return jsonify({"message": "Image 2 uploaded successfully"}), 200
    
    return jsonify({"error": "File format not allowed"}), 400

# Route untuk memprediksi kemiripan wajah
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Gunakan DeepFace untuk memverifikasi kemiripan wajah
        result = DeepFace.verify(os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg'),
                                 os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg'))
        
        # Mendapatkan nilai distance (semakin kecil semakin mirip)
        distance = result['distance']
        
        # Menghitung persentase kemiripan (semakin rendah distance, semakin tinggi persentasenya)
        similarity_percentage = (1 - distance) * 100

        return jsonify({"similarity_percentage": similarity_percentage}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
