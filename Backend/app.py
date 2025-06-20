import os
from flask import Flask, request, jsonify
from deepface import DeepFace
from werkzeug.utils import secure_filename
from flask_cors import CORS

# ==============================================================================
# INISIALISASI & KONFIGURASI APLIKASI
# ==============================================================================
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ==============================================================================
# FUNGSI HELPERS
# ==============================================================================
def allowed_file(filename):
    """Mengecek apakah format file diizinkan."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, filename):
    """Menyimpan file yang diunggah dengan aman."""
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filepath
    return None

# ==============================================================================
# ENDPOINT API INTI
# ==============================================================================
@app.route('/')
def index():
    return "Simple Face API is running!"

@app.route('/compare', methods=['POST'])
def compare_faces():
    """Membandingkan dua gambar yang diunggah dengan parameter tuning lengkap."""
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({"error": "Dua gambar diperlukan."}), 400

    file1 = request.files['image1']
    file2 = request.files['image2']
    
    # Ambil semua parameter tuning dari request form
    model_name = request.form.get('model_name', 'VGG-Face')
    detector_backend = request.form.get('detector_backend', 'opencv')
    distance_metric = request.form.get('distance_metric', 'cosine')

    img1_path = save_uploaded_file(file1, 'compare_1.jpg')
    img2_path = save_uploaded_file(file2, 'compare_2.jpg')

    if not img1_path or not img2_path:
        return jsonify({"error": "Format file tidak valid."}), 400

    try:
        # Teruskan semua parameter ke DeepFace.verify
        result = DeepFace.verify(
            img1_path=img1_path, 
            img2_path=img2_path, 
            model_name=model_name,
            detector_backend=detector_backend,
            distance_metric=distance_metric
        )

        distance = result.get('distance', 0)
        similarity = max(0, (1 - distance) * 100)

        return jsonify({
            "similarity_percentage": similarity,
            "verified": result.get('verified', False),
            "distance": distance,
            "model_used": result.get('model', model_name)
        }), 200
    except Exception as e:
        if "Face could not be detected" in str(e):
            return jsonify({"error": "Wajah tidak dapat terdeteksi di salah satu gambar."}), 400
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500

@app.route('/analyze', methods=['POST'])
def analyze_face():
    """Menganalisis satu gambar untuk emosi, umur, dan gender."""
    if 'image' not in request.files:
        return jsonify({"error": "Gambar diperlukan."}), 400

    file = request.files['image']
    img_path = save_uploaded_file(file, 'analyze_1.jpg')

    if not img_path:
        return jsonify({"error": "Format file tidak valid."}), 400

    try:
        # Panggil DeepFace.analyze dengan actions yang spesifik
        analysis_results = DeepFace.analyze(img_path, actions=['age', 'gender', 'emotion'])
        if not analysis_results:
            return jsonify({"error": "Tidak dapat menganalisis gambar."}), 400
        
        first_face = analysis_results[0]
        return jsonify({
            "age": first_face.get("age"),
            "gender": first_face.get("dominant_gender"),
            "emotion": first_face.get("dominant_emotion")
        }), 200
    except Exception as e:
        if "Face could not be detected" in str(e):
            return jsonify({"error": "Wajah tidak dapat terdeteksi dalam gambar."}), 400
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500

# ==============================================================================
# MENJALANKAN APLIKASI
# ==============================================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)