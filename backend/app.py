from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to the website'

@app.route('/chat')
def chat():
    return 'This is the chat home'

@app.route('/chat/find')
def findChat():
    return 'Looking for a chat...'

# Once chat found, will communicate with Twillio to connect
# Once ended, will redirect to chat

@app.route('/chat/survey')
def chatSurvey():
    return 'This is a chat survey'
    

if __name__ == '__main__':
    app.run()
