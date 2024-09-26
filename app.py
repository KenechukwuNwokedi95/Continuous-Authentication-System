from flask import Flask, request, jsonify, session, redirect, url_for, render_template
import joblib
import numpy as np
import os
import json

app = Flask(__name__)
app.secret_key = "nmtpllseet34gssce4t"

# Define the file path for the model
model_path = os.path.join(os.path.dirname(__file__), 'server/svm4_model (1).pkl')

# Load the trained model
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    raise FileNotFoundError(f"Model file not found: {model_path}")

users_db = {}


def calculate_metrics(key_events, scroll_events):
    dwell_times = []
    flight_times = []
    scroll_deltas = []

    for i, event in enumerate(key_events):
        if event['Event'] == 'pressed':
            key = event['Key']
            press_time = float(event['Epoch'])
            release_time = next((float(e['Epoch']) for e in key_events[i+1:] if e['Key'] == key and e['Event'] == 'released'), press_time)
            dwell_time = release_time - press_time
            dwell_times.append(dwell_time)

            if i > 0:
                previous_event = key_events[i-1]
                if previous_event['Event'] == 'pressed':
                    flight_time = press_time - float(previous_event['Epoch'])
                    flight_times.append(flight_time)
    
    for i in range(1, len(scroll_events)):
        delta_x = scroll_events[i]['ScrollX'] - scroll_events[i-1]['ScrollX']
        delta_y = scroll_events[i]['ScrollY'] - scroll_events[i-1]['ScrollY']
        scroll_deltas.append((delta_x, delta_y))
    
    average_trajectory = sum(dwell_times) / len(dwell_times) if dwell_times else 0
    average_scroll_delta = np.mean(scroll_deltas, axis=0) if scroll_deltas else (0, 0)
    
    return {
        'dwell_times': dwell_times,
        'flight_times': flight_times,
        'average_trajectory': average_trajectory,
        'average_scroll_delta': average_scroll_delta
    }
    
def save_user_data(username, key_events):
    user_dir = os.path.join(os.path.dirname(__file__), f'user_data/{username}')
    os.makedirs(user_dir, exist_ok=True)
    
    key_events_file = os.path.join(user_dir, 'key_events.json')
    #scroll_events_file = os.path.join(user_dir, 'scroll_events.json')
    
    with open(key_events_file, 'w') as f:
        json.dump(key_events, f, indent=4)
    
    #with open(scroll_events_file, 'w') as f:
        #json.dump(scroll_events, f, indent=4)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    key_events = data.get('key_events', [])
    scroll_events = data.get('scroll_events', [])
    
    # Check if username already exists (prevent duplicate registrations)
    if username in users_db:
        return jsonify({'message': 'Username already exists!'}), 200

    # Calculate keystroke metrics
    metrics = calculate_metrics(key_events, scroll_events)
    feature_vector = metrics['dwell_times'] + metrics['flight_times'] + [metrics['average_trajectory']] + list(metrics['average_scroll_delta'])

    users_db[username] = {
        'password': password,
        'keystroke_metrics': feature_vector
    }
    
    # Save user data
    save_user_data(username, key_events)

    session['username'] = username
    return jsonify({'message': 'Registration successful!'}), 201  # Created status code


@app.route('/auth_check', methods=['POST'])
def auth_check():
    if 'username' not in session:
        return jsonify({'message': 'Not authenticated!'}), 401
    
    username = session['username']
    
    data = request.get_json()
    key_events = data.get('key_events', [])
    scroll_events = data.get('scroll_events', [])
    metrics = calculate_metrics(key_events, scroll_events)
    feature_vector = metrics['dwell_times'] + metrics['flight_times'] + [metrics['average_trajectory']] + list(metrics['average_scroll_delta'])
    
    # Save user data
    save_user_data(username, key_events)
    
    if not key_events:  # No keystrokes, user is idle
        return jsonify({'message': 'User is idle, no authentication required.'}), 200
    
    registered_metrics = users_db[username]['keystroke_metrics']
    prediction = model.predict([feature_vector])
    
    if prediction[0] != 1:
        session.pop('username', None)
        return jsonify({'message': 'Session expired due to keystroke and scroll mismatch!'}), 401
    
    return jsonify({'message': 'Authentication successful!'}), 200

@app.route('/messaging', methods=['GET'])
def messaging():
    if 'username' not in session:
        return redirect(url_for('/login_page'))
    return render_template('chat.html', username=session['username'])


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    # Save or process the message as needed
    return jsonify({'message': 'Message sent successfully!'}), 200


@app.route('/', methods=['GET'])
def login_page():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)