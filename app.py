from flask import Flask, render_template, make_response, request, jsonify

import time

app = Flask(__name__)





@app.route('/')
def index():
    timestamp = int(time.time())
    return render_template('index.html', timestamp=timestamp)


@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message', '')
    bot_response = f"Hello! You said: {user_message}"  # Replace with AI logic
    return jsonify({'response': bot_response})




if __name__ == '__main__':
    app.run()