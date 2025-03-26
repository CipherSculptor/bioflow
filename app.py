from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, BioFlow! This is a test deployment.'

@app.route('/test')
def test():
    return {'status': 'ok', 'message': 'API is working'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 