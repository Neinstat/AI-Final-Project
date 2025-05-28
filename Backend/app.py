import os
from flask import Flask, request, jsonify
from deepface import DeepFace
from werkzeug.utils import secure_filename
from flask_cors import CORS
import cv2

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'HEIC'}

# Pastikan direktori UPLOAD_FOLDER ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return "Face Similarity API is running!"

# Fungsi untuk mendeteksi wajah dan memberi anotasi (menggunakan OpenCV)
def detect_face(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Warning: Could not read image at {image_path} for face detection.")
            return False # Menandakan gambar tidak bisa dibaca atau tidak ada wajah

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            print(f"Warning: No faces detected in {image_path}.")
            # Anda bisa memilih untuk tidak menyimpan ulang gambar jika tidak ada wajah,
            # atau mungkin mengembalikan status yang bisa ditangkap frontend.
            return False # Menandakan tidak ada wajah terdeteksi

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        cv2.imwrite(image_path, img) # Simpan gambar dengan kotak pembatas
        return True # Menandakan wajah terdeteksi
    except Exception as e:
        print(f"Error in detect_face for {image_path}: {str(e)}")
        return False


# Upload Gambar 1
@app.route('/upload_image1', methods=['POST'])
def upload_image1():
    if 'image1' not in request.files:
        return jsonify({"error": "No file part for image1"}), 400
    file1 = request.files['image1']
    
    if file1.filename == '':
        return jsonify({"error": "No selected file for image1"}), 400
    
    if file1 and allowed_file(file1.filename):
        # Selalu simpan sebagai image1.jpg untuk konsistensi
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
        file1.save(filepath1)
        
        # Opsional: periksa apakah wajah terdeteksi
        # if not detect_face(filepath1):
        #     return jsonify({"error": "No face detected in Image 1 or image could not be processed"}), 400
            
        return jsonify({"message": "Image 1 uploaded successfully"}), 200
    
    return jsonify({"error": "File format not allowed for image1"}), 400

# Upload Gambar 2
@app.route('/upload_image2', methods=['POST'])
def upload_image2():
    if 'image2' not in request.files:
        return jsonify({"error": "No file part for image2"}), 400
    file2 = request.files['image2']
    
    if file2.filename == '':
        return jsonify({"error": "No selected file for image2"}), 400
    
    if file2 and allowed_file(file2.filename):
        # Selalu simpan sebagai image2.jpg untuk konsistensi
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg')
        file2.save(filepath2)

        # Opsional: periksa apakah wajah terdeteksi
        # if not detect_face(filepath2):
        #     return jsonify({"error": "No face detected in Image 2 or image could not be processed"}), 400
            
        return jsonify({"message": "Image 2 uploaded successfully"}), 200
    
    return jsonify({"error": "File format not allowed for image2"}), 400


# Bandingkan dua foto
@app.route('/compare_photos', methods=['POST'])
def compare_photos():
    try:
        data = request.get_json()
        # Ambil model_name dari request, default ke 'DeepFace' jika tidak ada
        model_name_frontend = data.get('model_name', 'DeepFace') if data else 'DeepFace'

        print(f"Using model: {model_name_frontend} for comparison.") # Debugging print

        img1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
        img2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg')

        if not os.path.exists(img1_path) or not os.path.exists(img2_path):
            return jsonify({"error": "One or both images not found on server. Please upload again."}), 404

        # Lakukan perbandingan kemiripan wajah menggunakan DeepFace
        result = DeepFace.verify(
            img1_path,
            img2_path,
            model_name=model_name_frontend # Gunakan model yang dipilih dari frontend
        )
        print("Result from DeepFace.verify:", result)  # Debugging print

        distance = result.get('distance', 0) # Default distance jika tidak ada
        # Konversi distance ke persentase kemiripan. Formula ini umum, tapi threshold bisa bervariasi antar model.
        # Model seperti VGG-Face dan Facenet biasanya memiliki distance lebih rendah untuk wajah yang mirip.
        # Threshold untuk 'verified' true/false juga berbeda per model.
        # Untuk persentase yang intuitif: (1 - distance) * 100.
        # Jika distance bisa > 1 (untuk model tertentu yang tidak dinormalisasi), ini perlu penyesuaian.
        # Asumsi distance adalah antara 0 dan ~1.2 (atau 0 dan 2 untuk beberapa model),
        # di mana 0 adalah identik.
        
        # Normalisasi kasar untuk persentase:
        # Batasi distance agar tidak negatif, dan jika > 1, persentase akan negatif.
        # Mungkin lebih baik menampilkan distance secara langsung atau menggunakan verified flag.
        # Untuk tujuan ini, kita akan tetap menggunakan (1-distance)*100 tapi sadar akan batasannya.
        similarity_percentage = max(0, (1 - distance) * 100)


        return jsonify({
            "similarity_percentage": similarity_percentage,
            "verified": result.get('verified', False),
            "distance": distance,
            "model_used": model_name_frontend
        }), 200
    except ValueError as ve: # Khususnya jika DeepFace tidak menemukan wajah
        print(f"ValueError during comparison: {str(ve)}")
        return jsonify({"error": f"Could not process images: {str(ve)}. Ensure faces are clear and detectable."}), 400
    except Exception as e:
        print(f"Error during comparison: {str(e)}")  # Print error ke konsol
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# Analisis Usia, Gender, dan Emosi menggunakan DeepFace
@app.route('/analyze_photo', methods=['POST'])
def analyze_photo():
    try:
        img1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg') # Menggunakan image1.jpg untuk analisis
        
        if not os.path.exists(img1_path):
             return jsonify({"error": "Image for analysis not found. Please upload first."}), 404

        # Analisis menggunakan DeepFace untuk Prediksi Usia, Gender, dan Emosi
        # enforce_detection=False dapat ditambahkan jika ingin mencoba menganalisis meski wajah tidak terlalu jelas,
        # tapi bisa menghasilkan error jika wajah sama sekali tidak terdeteksi.
        analysis_results = DeepFace.analyze(
            img1_path,
            actions=['age', 'gender', 'emotion'],
            enforce_detection=True # Defaultnya True, pastikan wajah terdeteksi
        )
        
        # DeepFace.analyze mengembalikan list of dictionaries (satu per wajah)
        if not analysis_results or not isinstance(analysis_results, list) or len(analysis_results) == 0:
            return jsonify({"error": "Could not analyze image or no face detected."}), 400
            
        first_face_analysis = analysis_results[0] # Ambil hasil untuk wajah pertama yang terdeteksi
        
        age = first_face_analysis.get("age")
        gender = first_face_analysis.get("dominant_gender")
        emotion = first_face_analysis.get("dominant_emotion")
        
        return jsonify({
            "age": age,
            "gender": gender,
            "emotion": emotion
        }), 200
    except ValueError as ve: # Error jika DeepFace tidak dapat memproses (misal, tidak ada wajah)
        print(f"ValueError during analysis: {str(ve)}")
        return jsonify({"error": f"Could not process image: {str(ve)}. Ensure face is clear and detectable."}), 400
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred during analysis: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)