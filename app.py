from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS if needed

# Global transaction counter (for demonstration)
transaction_count = 1000

# In-memory queues for admin monitoring (optional)
queues = {
    "cashier": [],
    "registrar": []
}

# Route for the student page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')

# API endpoint to generate a transaction number
@app.route('/get_number', methods=['POST'])
def get_transaction_number():
    global transaction_count
    data = request.json
    student_id = data.get('student_id')
    department = data.get('department')
    
    if not student_id:
        return jsonify({'error': 'Student ID is required'}), 400
    if not department:
        return jsonify({'error': 'Department is required'}), 400

    transaction_count += 1
    tn_number = f"{department[:3].upper()}-{transaction_count}"
    
    # Add the entry to the appropriate queue for admin view
    queues[department].append({'id': student_id, 'number': tn_number})
    
    return jsonify({'transaction_number': tn_number})

# API endpoint to get queue data (for admin view)
@app.route('/queue_data')
def queue_data():
    return jsonify(queues)

# API endpoint to process the next number in a given department's queue
@app.route('/next_number', methods=['POST'])
def next_number():
    department = request.args.get('department')
    if department not in queues or not queues[department]:
        return jsonify({'message': f"No entries in {department} queue."})
    entry = queues[department].pop(0)
    return jsonify({'message': f"Processed {entry['number']} for Student ID: {entry['id']}"})

if __name__ == '__main__':
    app.run(debug=True)
