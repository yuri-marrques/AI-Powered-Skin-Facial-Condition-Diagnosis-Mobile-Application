# AI Powered Skin Facial Condition Diagnosis Mobile Application

An intelligent cross-platform mobile app that detects facial skin types and conditions using AI, then suggests skincare products and lifestyle adjustments. It helps users find the most compatible skincare products based on their skin profile and allergies.

## 🧠 Features

- Detects **facial skin type** (e.g. Oily, Dry, Combination).
- Detects **facial skin conditions** (e.g. Acne, Eczema, Rosacea).
- Suggests **skincare products** based on:
  - Detected skin type/condition
  - Product ingredients
  - User-uploaded allergens
- Provides **lifestyle advice** per skin type
- Face detection and cropping using OpenCV before AI diagnosis
- RESTful API backend in Flask, AI in Python, frontend in React Native (Expo)
- MongoDB database for data storage

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js & npm/yarn
- Expo CLI (`npm install -g expo-cli`)
- MongoDB (local or cloud instance)

### 1. Dataset Setup

Create the following folder structure inside the `server/` folder:

```
server/
└── datasets/
    ├── train/
    │   ├── Normal Skin/
    │   ├── Acne/
    │   └── ... (Other skin types and conditions)
    └── test/
        ├── Normal Skin/
        ├── Acne/
        └── ... (Same as above)
```

Each subfolder inside `train/` and `test/` should be named after a **skin type** or **skin disease**. Example names:
- `Normal Skin`
- `Oily Skin`
- `Eczema`
- `Rosacea`

> Train and test folders must contain the **same categories** for accurate evaluation.

---

### 2. Model Training

In `server/train.py`, update the number of classes:

```python
number_of_objects = <number of skin types and conditions>
```

To train the model:

```bash
cd server
pip install -r requirements.txt
python train.py
```

---

### 3. Starting the Backend Server

Once trained, start the Flask backend:

```bash
cd server
python app.py
```

---

### 4. Running the Frontend App

```bash
cd app
npm install
expo start
```

Scan the QR code with Expo Go or run on an emulator.

---

## 🧪 Diagnosis Flow

1. User uploads a selfie on the app.
2. The backend:
   - Detects the face using `cv2.CascadeClassifier`.
   - Crops the face and passes it to the trained model.
   - Returns:
     - Predicted skin type
     - Any detected skin conditions
     - Lifestyle suggestions (from a data dictionary)
     - Compatible skincare product recommendations (based on user's allergens)

---

## 📚 References

### Datasets

- [DermNet Skin Condition Images (Kaggle)](https://www.kaggle.com/shubhamgoel27/dermnet)
- [DermNet NZ Image Library](https://dermnetnz.org/image-library)

### Skin Type Guide
- https://www.today.com/style/5-different-skin-types-which-type-skin-do-you-have-t152786

### Skin Condition Reference
- https://dermnetnz.org/topics/facial-skin-problems

---

## 🎯 Project Objectives

- Detect facial **skin type**
- Identify **facial skin conditions**
- Recommend **skincare products** (filtered by allergies)
- Provide **lifestyle recommendations** based on skin type

---

## 🧬 Technologies Used

| Component  | Stack                        |
|------------|------------------------------|
| Frontend   | React Native + Expo          |
| Backend    | Python Flask (REST API)      |
| AI Model   | Python (custom CNN)          |
| Database   | MongoDB                      |
| Image Processing | OpenCV                  |

---

## 📂 .gitignore Recommendation

Add this to your `.gitignore`:

```
# Ignore dataset images
server/datasets/
```

Or, if only ignoring compressed versions:

```
server/datasets/compressed datasets/
```

---

## 🤝 Contributing

Please open issues or pull requests if you'd like to help improve the app!

---

## 📬 Contact

For support or feedback, email **michaelmudimbu@gmail.com**