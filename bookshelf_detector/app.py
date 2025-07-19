from flask import Flask, request, jsonify, render_template
from ultralytics import YOLO
import cv2
import numpy as np
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

model = YOLO('yolov8s.pt')

def init_db():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    results = model(img)
    annotated_img = results[0].plot()
    count = len(results[0].boxes)

    result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result.jpg')
    cv2.imwrite(result_path, annotated_img)

    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('INSERT INTO requests (timestamp, result) VALUES (?, ?)',
              (str(datetime.now()), json.dumps({'count': count})))
    conn.commit()
    conn.close()

    return jsonify(count=count)

if __name__ == '__main__':
    app.run(debug=True)
