#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import webbrowser
import threading
import os
import sys

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

print(f"DEBUG: base_path = {base_path}")
template_folder = os.path.join(base_path, "templates")
static_folder = os.path.join(base_path, "templates", "static")
print(f"DEBUG: template_folder = {template_folder}")
print(f"DEBUG: static_folder = {static_folder}")

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

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
    app.run(host='127.0.0.1', port=5001)

if __name__ == '__main__':
    main()
