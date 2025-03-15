from flask import Flask, render_template, make_response

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
    return render_template('index.html')




if __name__ == '__main__':
    app.run()