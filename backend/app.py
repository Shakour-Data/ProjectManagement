from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Initialize project data
projects = [
    {"project_id": "project-alpha", "name": "Project Alpha", "created_at": datetime.now().isoformat()},
    {"project_id": "project-beta", "name": "Project Beta", "created_at": datetime.now().isoformat()},
    {"project_id": "project-gamma", "name": "Project Gamma", "created_at": datetime.now().isoformat()}
]

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    return jsonify(projects)

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create new project"""
    data = request.get_json()
    
    if not data or 'project_id' not in data:
        return jsonify({"error": "project_id is required"}), 400
    
    project_id = data['project_id']
    
    # Check for duplicate project
    existing_project = next((p for p in projects if p['project_id'] == project_id), None)
    if existing_project:
        return jsonify({"error": "Project already exists"}), 409
    
    new_project = {
        "project_id": project_id,
        "name": project_id,
        "created_at": datetime.now().isoformat()
    }
    
    projects.append(new_project)
    return jsonify(new_project), 201

@app.route('/api/projects', methods=['DELETE'])
def delete_project():
    """Delete project"""
    project_id = request.args.get('project_id')
    
    if not project_id:
        return jsonify({"error": "project_id is required"}), 400
    
    project_to_remove = next((p for p in projects if p['project_id'] == project_id), None)
    if not project_to_remove:
        return jsonify({"error": "Project not found"}), 404
    
    projects.remove(project_to_remove)
    return jsonify({"message": "Project deleted successfully"}), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "OK",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
