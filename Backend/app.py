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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return "Face Similarity API is running!"

# Upload Image 1
@app.route('/upload_image1', methods=['POST'])
def upload_image1():
    if 'image1' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file1 = request.files['image1']
    
    if file1.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file1 and allowed_file(file1.filename):
        filename1 = secure_filename(file1.filename)
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
        file1.save(filepath1)
        
        # Face Detection Feedback
        detect_face(filepath1)
        return jsonify({"message": "Image 1 uploaded successfully"}), 200
    
    return jsonify({"error": "File format not allowed"}), 400

# Upload Image 2
@app.route('/upload_image2', methods=['POST'])
def upload_image2():
    if 'image2' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file2 = request.files['image2']
    
    if file2.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file2 and allowed_file(file2.filename):
        filename2 = secure_filename(file2.filename)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg')
        file2.save(filepath2)
        
        # Face Detection Feedback
        detect_face(filepath2)
        return jsonify({"message": "Image 2 uploaded successfully"}), 200
    
    return jsonify({"error": "File format not allowed"}), 400

# Face detection and annotation (using OpenCV)
def detect_face(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Load OpenCV pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    # Save the image with bounding boxes
    cv2.imwrite(image_path, img)

# Compare two photos
@app.route('/compare_photos', methods=['POST'])
def compare_photos():
    try:
        # Perform face similarity comparison using DeepFace
        result = DeepFace.verify(
            os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg'),
            os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg'),
            model_name='DeepFace'
        )
        print("Result:", result)  # Debugging print

        # Get the distance and calculate similarity percentage
        distance = result['distance']
        similarity_percentage = (1 - distance) * 100

        return jsonify({
            "similarity_percentage": similarity_percentage,
            "model_used": 'DeepFace'
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")  # Print the error to console
        return jsonify({"error": str(e)}), 500



# Analyze Age, Gender, and Emotion using DeepFace
@app.route('/analyze_photo', methods=['POST'])
def analyze_photo():
    try:
        # Analyze using DeepFace for Age, Gender, and Emotion Prediction
        analysis = DeepFace.analyze(
            os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg'),
            actions=['age', 'gender', 'emotion']
        )
        
        # Extract the results
        age = analysis[0]["age"]
        gender = analysis[0]["dominant_gender"]
        emotion = analysis[0]["dominant_emotion"]
        
        return jsonify({
            "age": age,
            "gender": gender,
            "emotion": emotion
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
