#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import webbrowser
import threading
import os
import sys

app = Flask(__name__, static_folder='ui/static', template_folder='ui')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/install', methods=['POST'])
def install():
    # Here you can add the installation logic
    data = request.json
    # For demonstration, just echo back the received data
    return jsonify({"status": "success", "message": "Installation started", "data": data})

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

def main():
    threading.Timer(1, open_browser).start()
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    main()
