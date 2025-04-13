from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# --- Sample Data for 6 Parking Slots ---
# For demonstration, each refresh randomly assigns True/False to a slot
# meaning "True" = slot is free, "False" = slot is occupied
@app.route('/api/parking_data')
def parking_data():
    slots = [
        {"slot_id": 1, "is_free": bool(random.getrandbits(1))},
        {"slot_id": 2, "is_free": bool(random.getrandbits(1))},
        {"slot_id": 3, "is_free": bool(random.getrandbits(1))},
        {"slot_id": 4, "is_free": bool(random.getrandbits(1))},
        {"slot_id": 5, "is_free": bool(random.getrandbits(1))},
        {"slot_id": 6, "is_free": bool(random.getrandbits(1))},
    ]
    return jsonify(slots)

# --- MAIN PAGE: Project Description ---
@app.route('/')
def index():
    return render_template('index.html')

# --- DASHBOARD PAGE: Visualization, metrics, etc. ---
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# --- TEAM PAGE: Team and members ---
@app.route('/team')
def page_team():
    return render_template('page_team.html')

if __name__ == '__main__':
    # For development on your PC, you can keep '127.0.0.1'.
    # For Raspberry Pi deployment, consider '0.0.0.0' so it's accessible on your local network.
    app.run(debug=True, host='127.0.0.1', port=5000)
