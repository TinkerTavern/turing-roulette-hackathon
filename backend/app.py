from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to the website'

@app.route('/chat')
def chat():
    return 'Connecting you to a \'user\'..'

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
