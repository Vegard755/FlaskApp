from flask import Flask, render_template, make_response, request, jsonify
import time
import os
from dotenv import load_dotenv
from flask_cors import CORS
from google import genai
from google.genai.errors import ServerError


app = Flask(__name__)
CORS(app)




load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")


@app.route('/')
def index():
    timestamp = int(time.time())
    return render_template('index.html', timestamp=timestamp)


@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message')
    print(user_message)
    format_string = gemini_inputs(user_message)
    
    client = genai.Client(api_key=GOOGLE_API_KEY)
    try:
        response = client.models.generate_content(model="tunedModels/username-generator-m2q467sj0qcm", contents=format_string)
    except ServerError as e:
        return jsonify({"response": "Server Error. Please try again."})
    raw_response = response.text

    cleaned_usernames = []
    for line in raw_response.splitlines():
        cleaned_line = line.lstrip("0123456789-. ").strip()
        if cleaned_line:
            cleaned_usernames.append(cleaned_line)
    
    cleaned_response = "\n".join(cleaned_usernames)
    print(cleaned_response)
    
    return jsonify({"response": cleaned_response})


def gemini_inputs(user_message):
    name_list = [
        "VelocityX", "Panzer", "Khanada", "Sky", "Cented", "Fredoxie", "Hris", "Idrop", "Mitr0", "Mero", "Mongraal", 
        "Benjyfishy", "Clix", "Bugha", "Zayt", "Bizzle", "Dubs", "S4f", "Stretch", "Jamper", "Nickmercs", "Tfue", "Letshe",
        "Epikwhale", "Nate Hill", "Reverse2k", "Aqua", "Stompy", "MrSavage", "Snayzy", "JannisZ", "Kinstaar", "Fray", "Mappi",
        "Kiryache32", "Tayson", "Wolfiez", "Vorwenn", "Andilex", "4zr", "Nyhrox", "Crr", "Rezon", "Saevid", "Flikk", "Anas",
        ]
    name_string = ", ".join(name_list)

    prompt = f"""
    You are my username generator. You need to generate me 10 creative and clean usernames based on this: {user_message}. 
    For inspirational purposes, here are some good usernames, and remember, dont copy them, theyre only for inspiration:
    {name_string}.
    Some of the names you generate has to be 'one worded', and some can be 'two worded'.
    Only give me the usernames, no other text.
    """


    no_message_string = f"""
    You are my username generator. You need to generate me 10 creative and clean usernames. 
    For inspirational purposes, here are some good usernames, and remember, dont copy them, theyre only for inspiration:
    {name_string}.
    Some of the names you generate has to be 'one worded': "Fredoxie" and some can be 'two worded': "Nate Hill".
    Only give me the usernames, no other text.
    """

    if user_message == "" or user_message == None:
        return no_message_string
    else:
        return prompt








if __name__ == '__main__':
    app.run(debug=True)