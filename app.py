from flask import Flask, render_template, make_response, request, jsonify

import time

app = Flask(__name__)

def nocache(view):
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return no_cache




@app.route('/')
@nocache
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