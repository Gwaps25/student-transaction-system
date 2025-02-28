from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS if your frontend is served from a different domain

# Global transaction counter (for demo purposes)
transaction_count = 1000

# A simple in-memory queue for demonstration (optional)
queues = {
    "cashier": [],
    "registrar": []
}

@app.route('/')
def home():
    return render_template('index.html')

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

    # Generate Transaction Number
    transaction_count += 1
    tn_number = f"{department[:3].upper()}-{transaction_count}"
    
    # Optional: Append the entry to a queue list (for admin monitoring)
    queues[department].append({'id': student_id, 'number': tn_number})
    
    return jsonify({'transaction_number': tn_number})

# Optional route for the admin view to update queue info
@app.route('/queue_data')
def queue_data():
    return jsonify(queues)

# Optional: Route to simulate processing next number in queue
@app.route('/next_number', methods=['POST'])
def next_number():
    department = request.args.get('department')
    if department not in queues or not queues[department]:
        return jsonify({'message': f"No entries in {department} queue."})
    entry = queues[department].pop(0)
    return jsonify({'message': f"Processed {entry['number']} for Student ID: {entry['id']}"})

if __name__ == '__main__':
    app.run(debug=True)
