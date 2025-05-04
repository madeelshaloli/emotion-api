from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import os
import cv2

app = Flask(__name__)
CORS(app)

@app.route('/emotion', methods=['POST'])
def detect_emotion():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    image_path = "temp.jpg"
    image.save(image_path)

    try:
        # Detect face and extract cropped face image
        detections = DeepFace.extract_faces(img_path=image_path, enforce_detection=True)

        if not detections:
            return jsonify({'error': 'No face detected'}), 400

        # Convert and save cropped face
        face_img = detections[0]['face']
        face_img_uint8 = (face_img * 255).astype("uint8")
        face_path = "temp_face.jpg"
        cv2.imwrite(face_path, cv2.cvtColor(face_img_uint8, cv2.COLOR_RGB2BGR))

        # Analyze emotion on cropped face
        result = DeepFace.analyze(img_path=face_path, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']

        os.remove(image_path)
        os.remove(face_path)

        return jsonify({'emotion': emotion})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

