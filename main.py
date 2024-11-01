from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'home'

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0')