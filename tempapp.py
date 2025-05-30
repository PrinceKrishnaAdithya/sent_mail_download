from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)

# Allow requests from local frontend (Outlook add-in)
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5000", "http://localhost"])

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # Consider locking this in production
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    return response

@app.route('/receive_email', methods=['GET'])
def test_page():
    return "This endpoint expects POST requests with email data."

@app.route('/receive_email', methods=['POST'])

def handle_email():
    print("📩 Received POST to /receive_email")

    data = request.get_json(silent=True)

    print("🧾 Headers:", request.headers)
    print("🔍 Is JSON:", request.is_json)
    print("📦 JSON Data:", data)

    if data:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"email_{timestamp}.json"
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Saved to file: {filename}")
        return jsonify({"status": "success"}), 200
    else:
        print("❌ Invalid JSON received.")
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

@app.route('/')
def home():
    return "✅ Flask server is running!"

if __name__ == "__main__":
    app.run(port=5000)
