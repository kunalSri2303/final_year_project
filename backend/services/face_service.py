import cv2
import numpy as np
import base64
from fer import FER

# Initialize FER globally so it loads once
# use mtcnn=False for faster but slightly less accurate detection
detector = FER(mtcnn=False)

def analyze_face(base64_image: str) -> dict:
    try:
        # Check if the string contains the data URI scheme padding
        if "," in base64_image:
            base64_image = base64_image.split(",")[1]
            
        # Decode base64 to image
        img_data = base64.b64decode(base64_image)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detect emotions
        emotions = detector.detect_emotions(img)
        
        if not emotions:
            return {
                "emotion": "neutral",
                "confidence": 1.0,
                "all_emotions": {"neutral": 1.0}
            }
            
        # Get the first face's emotions
        emotions_dict = emotions[0]["emotions"]
        
        # Get top emotion
        top_emotion, score = detector.top_emotion(img)
        
        return {
            "emotion": top_emotion if top_emotion else "neutral",
            "confidence": score if score else 1.0,
            "all_emotions": emotions_dict
        }
    except Exception as e:
        print(f"Error analyzing face: {e}")
        return {
            "emotion": "neutral",
            "confidence": 1.0,
            "all_emotions": {"neutral": 1.0}
        }
