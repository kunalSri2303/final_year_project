from transformers import pipeline

# Initialize globally
try:
    classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", return_all_scores=True)
except Exception as e:
    print(f"Failed to load text emotion model: {e}")
    classifier = None

def analyze_text(text: str) -> dict:
    if not classifier:
        return {
            "emotion": "neutral",
            "confidence": 1.0,
            "all_emotions": {"neutral": 1.0}
        }
        
    try:
        results = classifier(text)
        
        # results is a list of lists: [[{'label': 'sadness', 'score': 0.9}, ...]]
        scores = results[0]
        
        all_emotions = {item['label']: item['score'] for item in scores}
        
        # Find top emotion
        top_emotion = max(scores, key=lambda x: x['score'])
        
        return {
            "emotion": top_emotion['label'],
            "confidence": top_emotion['score'],
            "all_emotions": all_emotions
        }
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return {
            "emotion": "neutral",
            "confidence": 1.0,
            "all_emotions": {"neutral": 1.0}
        }
