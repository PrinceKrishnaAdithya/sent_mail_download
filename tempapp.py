from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    return response

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/receive_email', methods=['GET'])
def test_page():
    return "This endpoint expects POST requests with email data."

@app.route('/receive_email', methods=['POST'])
def handle_email():
    print("📩 Received POST to /receive_email")

    try:
        subject = request.form.get("subject", "")
        body = request.form.get("body", "")
        to = request.form.get("to", "")
        from_ = request.form.get("from", "")
        cc = request.form.get("cc", "")
        bcc = request.form.get("bcc", "")
        attachments = request.files.getlist("attachments")

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        base_filename = f"email_{timestamp}"

        # Save metadata
        email_data = {
            "from": json.loads(from_),
            "to": json.loads(to),
            "cc": json.loads(cc),
            "bcc": json.loads(bcc),
            "subject": subject,
            "body": body,
            "attachments": [att.filename for att in attachments]
        }

        json_path = f"{base_filename}.json"
        with open(json_path, "w", encoding='utf-8') as f:
            json.dump(email_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Saved email metadata: {json_path}")

        # Save attachments
        for i, file in enumerate(attachments):
            filename = f"{base_filename}_att{i+1}_{file.filename}"
            file.save(filename)
            print(f"📎 Saved attachment: {filename}")

        return jsonify({"status": "success", "saved": base_filename}), 200

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)

