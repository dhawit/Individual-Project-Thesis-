import joblib

try:
    svd_model = joblib.load('/Users/dhawit/Downloads/svd_model.pkl')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
