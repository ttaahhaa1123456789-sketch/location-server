from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# فایل ذخیره‌سازی موقت
DATA_FILE = "data.json"

# اگر فایل وجود نداشت، یک فایل خالی بساز
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

@app.route('/location', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        # دریافت موقعیت جدید
        data = request.get_json()
        phone = data.get('phone')
        lat = data.get('lat')
        lng = data.get('lng')

        if not phone or lat is None or lng is None:
            return jsonify({"error": "Missing data"}), 400

        # خواندن دیتای فعلی
        with open(DATA_FILE, 'r') as f:
            users = json.load(f)

        # آپدیت کردن موقعیت کاربر
        users[phone] = {"lat": lat, "lng": lng}
        
        # ذخیره در فایل
        with open(DATA_FILE, 'w') as f:
            json.dump(users, f)

        return jsonify({"status": "ok"}), 200

    else:
        # دریافت همه موقعیت‌ها
        with open(DATA_FILE, 'r') as f:
            users = json.load(f)
        return jsonify(users), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
