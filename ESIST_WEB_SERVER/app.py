from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Sample endpoint to send dynamic metric data (for testing dynamic updates)
@app.route('/api/parking')
def parking_data():
    # Generate sample data: number of free parking slots out of 100
    free_slots = random.randint(0, 100)
    return jsonify({
        'free_slots': free_slots,
        'total_slots': 100
    })

# Main route serving our dashboard page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Run on localhost for development; later change host to '0.0.0.0' for Pi deployment.
    app.run(debug=True, host='127.0.0.1', port=5000)
