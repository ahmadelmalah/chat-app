from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

@app.route('/health-check')
def hello():
    resp = {}
    resp['it'] = 'works'
    return resp

@app.route('/chat')
def chat():
    server_url = 'http://127.0.0.1:8000'
    endpoint = server_url + '/messages/'
    res = requests.get(endpoint)
    messages = res.json()['messages']
    return render_template('chat.html', messages=messages)

@app.route('/send', methods=['POST'])
def send():
    server_url = 'http://127.0.0.1:8000'
    server_url = server_url + '/messages/'
    message = request.form['message']
    res = requests.post(server_url, json={"sender": "Ahmad", "body": message})
    return redirect('/chat')

if __name__ == '__main__':
    app.debug = True
    app.run()
