from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

DATABASE = 'references.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE "references" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                language TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add some sample data
        samples = [
            ('Print to Console', 'Python', 'print("Hello, World!")', 'python'),
            ('Hello World', 'JavaScript', 'console.log("Hello, World!");', 'javascript'),
            ('Docker Basics', 'Docker', 'docker run image_name\ndocker ps\ndocker build -t name .', 'bash'),
            ('Git Commit', 'Git', 'git add .\ngit commit -m "message"\ngit push', 'bash'),
        ]
        
        for title, category, content, lang in samples:
            cursor.execute('''
                INSERT INTO "references" (title, category, content, language)
                VALUES (?, ?, ?, ?)
            ''', (title, category, content, lang))
        
        conn.commit()
        conn.close()

@app.route('/api/references', methods=['GET'])
def get_references():
    search = request.args.get('search', '').lower()
    category = request.args.get('category', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM "references" WHERE 1=1'
    params = []
    
    if search:
        query += ' AND (title LIKE ? OR content LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    cursor.execute(query, params)
    refs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(refs)

@app.route('/api/references', methods=['POST'])
def create_reference():
    data = request.json
    
    if not data.get('title') or not data.get('content') or not data.get('category'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO "references" (title, category, content, language)
        VALUES (?, ?, ?, ?)
    ''', (data['title'], data['category'], data['content'], data.get('language', '')))
    
    conn.commit()
    ref_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': ref_id, 'message': 'Reference created'}), 201

@app.route('/api/references/<int:ref_id>', methods=['GET'])
def get_reference(ref_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM "references" WHERE id = ?', (ref_id,))
    ref = cursor.fetchone()
    conn.close()
    
    if not ref:
        return jsonify({'error': 'Not found'}), 404
    
    return jsonify(dict(ref))

@app.route('/api/references/<int:ref_id>', methods=['PUT'])
def update_reference(ref_id):
    data = request.json
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE "references" 
        SET title = ?, category = ?, content = ?, language = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (data.get('title'), data.get('category'), data.get('content'), 
          data.get('language', ''), ref_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Reference updated'})

@app.route('/api/references/<int:ref_id>', methods=['DELETE'])
def delete_reference(ref_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM "references" WHERE id = ?', (ref_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Reference deleted'})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT category FROM "references" ORDER BY category')
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(categories)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path and os.path.exists(os.path.join('static', path)):
        return send_from_directory('static', path)
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
