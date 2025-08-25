# AI-Powered Facial Skin Diagnosis & Smart Skincare Mobile App

[![Releases](https://img.shields.io/badge/Downloads-Releases-blue?logo=github&style=for-the-badge)](https://github.com/yuri-marrques/AI-Powered-Skin-Facial-Condition-Diagnosis-Mobile-Application/releases)

![Hero: Mobile Skin Analysis](https://images.unsplash.com/photo-1543349681-7a1a6fd7b9b3?auto=format&fit=crop&w=1400&q=80)

Quick links
- Releases (download and execute release asset): https://github.com/yuri-marrques/AI-Powered-Skin-Facial-Condition-Diagnosis-Mobile-Application/releases
- Topics: ai · computer-vision · deep-learning · dermatology · expo · face-detection · flask · fullstack · health-tech · image-classification · javascript · mobile-app · mongodb · open-cv · python · react-native · recommendation-system · skin-analysis · skin-care

What this repo does
- Detects face in a photo using OpenCV.
- Classifies skin type and conditions using a CNN.
- Builds a user skin profile with allergies and current products.
- Recommends products and lifestyle tips based on the profile.
- Runs on iOS and Android using React Native (Expo).
- Hosts model and API on a Flask backend with MongoDB persistence.

Why it matters
- Dermatology access varies by region. This app gives users a data-driven skin overview. It supports triage and self-care. It does not replace a medical exam. The project focuses on practical detection, product matching, and lifestyle guidance.

Demo images
- App mockup: https://images.unsplash.com/photo-1509395076047-4a66953f2bff?auto=format&fit=crop&w=1200&q=80
- Face detection sample: https://upload.wikimedia.org/wikipedia/commons/3/3f/OpenCV_Logo_with_text.png

Features
- Face detection with OpenCV and landmark checks.
- CNN-based image classification for skin condition labels (e.g., acne, rosacea, eczema, hyperpigmentation, normal/dry/oily/combination).
- Allergy and product blacklist in the user profile.
- Rule-based and collaborative filtering recommendation engine.
- Lifestyle guidance: sun protection, hydration, sleep, diet.
- Offline-first mobile client with sync to backend.
- Secure user data storage in MongoDB Atlas (configurable).
- Exportable reports and shareable product lists.

Tech stack
- Frontend: React Native (Expo), JavaScript, Expo Camera, React Navigation.
- Backend: Flask, Python 3.9+, Flask-RESTful, Gunicorn.
- ML: OpenCV for pre-processing, Keras/TensorFlow CNN for classification.
- Database: MongoDB (Atlas or local).
- DevOps: Docker, GitHub Actions for CI, optional Heroku/GCP deployment.
- Data formats: JSON API, multipart image uploads.

Architecture overview
- Mobile client captures or selects an image and sends it to the Flask API.
- The API runs face detection with OpenCV. If a face is valid, it runs the CNN model.
- The model returns labels and confidence scores.
- The backend fetches the user profile and runs the recommendation engine.
- Results return to the app for display. The app stores history locally and syncs with MongoDB.

Quick start (development)
1. Clone the repo.
2. Backend setup
   - Create a Python 3.9 virtual env.
   - Install: pip install -r backend/requirements.txt
   - Set env variables: MONGO_URI, FLASK_ENV=development, SECRET_KEY
   - Run: flask run --port 5000
3. Frontend setup
   - cd frontend
   - npm install
   - Start Expo: expo start
4. Mobile: open the Expo app on your phone or use an emulator.

Commands (examples)
- Start backend (dev)
  - flask run
- Start backend (production with Gunicorn)
  - gunicorn -w 4 -b 0.0.0.0:5000 app:app
- Start frontend
  - expo start --tunnel

Releases
- Download and execute the release file linked on the Releases page. The page contains packaged mobile builds (APK/IPA or Expo bundles) and backend bundles. Download the asset that matches your platform and follow the included README or installer steps. If a binary or installer is provided, run it on the target device or server.  
- Releases page: https://github.com/yuri-marrques/AI-Powered-Skin-Facial-Condition-Diagnosis-Mobile-Application/releases

API overview
- POST /api/v1/analyze
  - Accepts multipart form with field image and optional user_id.
  - Returns: face_detected, labels [{name, confidence}], skin_type, recommendations.
- GET /api/v1/profile/:id
  - Returns user profile, allergy list, product history.
- POST /api/v1/profile
  - Create or update a profile with allergies and product lists.
- GET /api/v1/products
  - Returns curated products with matched ingredients.
- POST /api/v1/feedback
  - Collects user feedback to update recommendation weights.

Sample response
{
  "face_detected": true,
  "labels": [
    {"name": "acne", "confidence": 0.86},
    {"name": "oily", "confidence": 0.72}
  ],
  "skin_type": "Oily",
  "recommendations": {
    "products": [{"id":"p123","score":0.92,"reason":"Non-comedogenic; targets acne"}],
    "lifestyle": ["Use SPF 50 daily", "Reduce dairy intake"]
  }
}

Model and data
- Model: Custom CNN (ResNet-style blocks) built in Keras. The final model outputs multi-label predictions for conditions and single-label output for skin type. The network uses transfer learning from EfficientNet-B0 for feature extraction and a custom head for the domain.
- Input: 224x224 RGB images after face crop and normalized pixel values.
- Training dataset: aggregated and anonymized mix of public dermatology datasets and private labeled samples. Augmentation used: rotation, flip, color jitter, brightness/contrast.
- Metrics: Precision, recall, F1 per label. Skin type classification reports overall accuracy.
- Performance goals: >85% macro F1 for common labels in controlled sets. Validation and test results live in the model/metrics folder.

Model files
- Training code: /ml/train.py
- Model definition: /ml/model.py
- Pretrained weights for inference: stored in releases and in /ml/checkpoints for dev use.

Recommendation engine
- Hybrid approach: rule-based filters plus collaborative filtering.
- Ingredient blacklist uses user allergies and avoid-list.
- Product scoring factors: ingredient match, comedogenic score, user reviews, price, brand suitability.
- Recommendations include reason strings to explain the match.

Privacy and data handling
- Store only images the user allows. The app supports on-device caching and user-controlled cloud sync.
- Remove images on request. The backend exposes a DELETE profile endpoint which removes images and history.
- Use HTTPS for all API calls. Use access tokens for user sessions.

Testing
- Unit tests for backend: pytest suite in backend/tests.
- Integration tests: Postman collection in tools/postman.
- Mobile tests: Jest for unit tests, Detox for end-to-end on Android and iOS.

CI/CD
- GitHub Actions run lint, unit tests, and build the backend container.
- Releases include automated build artifacts for mobile and server. Check the Releases page and download the relevant asset to run the app or server.

Screenshots
- App home and analyze flow: https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=1200&q=80
- Results view: https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=1200&q=80

Development tips
- Use Expo dev client for fast iteration on native APIs.
- Keep model inference off the main UI thread. Use background tasks for uploads and inference.
- Validate face crop size before sending to the model. Reject images with too small faces.
- Use a simple rate limiter on the API to avoid abuse.

Contributing
- Open issues for bugs or feature requests.
- Fork the repo and send pull requests against the main branch.
- Follow the code style in .editorconfig and run linters before commit.
- Add tests for new features and link them in your PR description.

Testing checklist
- Camera permission flows on iOS and Android.
- Face detection on varied lighting.
- Model output for edge cases like masks and glasses.
- Recommendation blacklist behavior for allergies.

Troubleshooting
- Backend CORS: ensure FRONTEND_ORIGIN is in CORS_ALLOW env var.
- Mongo connection: verify MONGO_URI and network rules.
- Expo build fails: update expo-cli to the latest matching SDK.
- Model mismatch: ensure the uploaded model matches the inference code in /ml/inference.py.

License
- MIT License (see LICENSE file).

Acknowledgements
- Open datasets in dermatology and public models.
- OpenCV contributors and the TensorFlow community.
- UI icon sets from public domain and Unsplash for demo imagery.

Contact and maintainers
- Maintainer: yuri-marrques (see the repo for full contact info).
- For urgent issues open an issue with the label "priority".

Badges
[![Python](https://img.shields.io/badge/Python-3.9+-blue)]()
[![React Native](https://img.shields.io/badge/React_Native-Expo-green)]()
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248)]()

Legal and medical
- The app provides informational content and product suggestions. For medical advice consult a licensed professional. The repo includes a privacy guide and data removal endpoint.

Extras
- Export report to PDF in the app.
- CSV export of product matches for dieticians and cosmetologists.
- Admin dashboard for product and model management in the web portal.

Releases reminder
- Download and execute the release asset from: https://github.com/yuri-marrques/AI-Powered-Skin-Facial-Condition-Diagnosis-Mobile-Application/releases