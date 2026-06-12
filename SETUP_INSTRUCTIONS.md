# 🎵 Moodify Setup & Execution Instructions

This project consists of an Emotion-Based Music Recommendation System with a FastAPI backend and a React (Vite) frontend.

## 1. Prerequisites
- Python 3.9+
- Node.js 20+ (Node 22.12 or Vite 5 compat recommended)
- (Optional) Spotify Developer Account for live song data

## 2. Directory Structure Overview
- `backend/`: FastAPI application containing all Agents, Services, Models, and DB.
- `frontend/`: React + Vite application containing all UI components and styling.

---

## 3. How to Run the Backend (FastAPI + AI Models)

Open a terminal and navigate to the project root (`final_year_project`):

```bash
# Navigate to backend
cd backend

# Create a virtual environment (if not already created)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server on port 8000
uvicorn main:app --port 8000 --reload
```

*The backend will automatically create an SQLite database (`recommender.db`) in the `backend` folder upon first startup.*

### 🔑 Connecting the Spotify API (Optional but Recommended)
By default, the backend will return "Mock" dummy data if Spotify credentials are not provided.
To connect real music:
1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) and create an app.
2. In the `backend` folder, create a file named `.env`.
3. Add the following lines to `.env`:
   ```env
   SPOTIFY_CLIENT_ID="your_client_id_here"
   SPOTIFY_CLIENT_SECRET="your_client_secret_here"
   ```
4. Restart the backend server.

---

## 4. How to Run the Frontend (React UI)

Open a *new* separate terminal and navigate to the project root:

```bash
# Navigate to frontend
cd frontend

# Install exact node modules (legacy peer deps required for some vite configurations)
npm install --legacy-peer-deps

# Start the Vite development server
npm run dev
```

*The frontend will start at `http://localhost:5173/` by default.*

---

## 5. How the Frontend Connects to the Backend 🔌

Under the hood, the backend API runs independently from the frontend webpage. They communicate over HTTP/WebSockets:
1. **The Backend Setup (CORS)**: In `backend/main.py`, FastAPI uses `CORSMiddleware` to authorize requests coming from the React application origin port (5173).
2. **The Frontend Setup (Fetch)**: In `frontend/src/App.jsx`, there is a variable `const API_BASE = "http://localhost:8000/api";`.
3. Whenever you trigger an action (like text detection), a React function performs an async Javascript `fetch()` call (like an invisible browser) sending your payload exactly to that endpoint:
   ```javascript
   const res = await fetch(`${API_BASE}/text-emotion`, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ text })
   });
   ```
4. The Python server receives it, the active Agent pipeline executes logic (Huggingface transformers), and FastAPI returns a JSON response matching the Pydantic schema schemas that React safely renders down.

---

## 5. How to Test the Application Cases

### Case 1: Text-Based Emotion Recognition
1. Open `http://localhost:5173/` in your browser.
2. Under the input section, click on the **Text Input** tab.
3. Type a sentence indicating emotion (e.g., *"I'm feeling so happy and energized today!"* or *"I am really stressed about exams"*).
4. Click **Detect Emotion**.
5. Wait for the HuggingFace `distilbert` pipeline to classify the text. You will see an Emoji and a Confidence bar pop up.
6. Beneath that, the grid will populate with recommended Spotify tracks matching that mood.

### Case 2: Facial Emotion Recognition
1. Open the app and ensure the **Camera** tab is selected first.
2. Click **Enable Camera** (You may need to allow browser permissions to use the webcam).
3. Frame your face in the box and make a distinct expression (smile, frown, surprise).
4. Click **Snap & Detect**.
5. The `fer` machine learning backend will detect your facial state.
6. The UI will render your mood and populate tracks mirroring your emotion.

### Case 3: Interaction Review
1. After interacting a baseline of emotions, click the **📚 Interaction History** accordion at the bottom of the page.
2. Here you can verify backend persistence, showing timelines alongside how many tracks were historically recommended out of the `sqlite` database.

*(Note: During the very first inference on the backend, the HuggingFace models may download locally, which takes ~260MB of data. Subsequent requests run instantly.)*
