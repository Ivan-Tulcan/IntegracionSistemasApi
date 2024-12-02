from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

# Base de datos en memoria
tasks = [
    {"id": 1, "title": "Comprar comida", "description": "Ir al supermercado", "status": "pendiente"},
    {"id": 2, "title": "Estudiar Flask", "description": "Desarrollar una API RESTful", "status": "en progreso"}
]

# Obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Listar todas las tareas
    ---
    responses:
      200:
        description: Lista de todas las tareas
    """
    return jsonify(tasks), 200

# Obtener una tarea por ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Consultar una tarea por ID
    ---
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Detalles de la tarea
      404:
        description: Tarea no encontrada
    """
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Tarea no encontrada"}), 404

# Crear una nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Crear una nueva tarea
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            status:
              type: string
    responses:
      201:
        description: Tarea creada exitosamente
      400:
        description: Datos inválidos
    """
    data = request.get_json()
    if not data.get('title') or not data.get('status'):
        return jsonify({"error": "Datos inválidos"}), 400
    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "description": data.get("description", ""),
        "status": data["status"]
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Actualizar una tarea existente
@app.route('/tasks/<int:task_id>', methods=['PUT', 'PATCH'])
def update_task(task_id):
    """
    Actualizar una tarea existente
    ---
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            status:
              type: string
    responses:
      200:
        description: Tarea actualizada exitosamente
      404:
        description: Tarea no encontrada
      400:
        description: Datos inválidos
    """
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    task.update(data)
    return jsonify(task), 200

# Eliminar una tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Eliminar una tarea
    ---
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Tarea eliminada exitosamente
      404:
        description: Tarea no encontrada
    """
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Tarea eliminada exitosamente"}), 200

if __name__ == '__main__':
    app.run(debug=True)
