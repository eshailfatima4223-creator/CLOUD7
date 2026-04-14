from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

tasks = []
task_id_counter = 1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def add_task():
    global task_id_counter
    data = request.get_json()
    task = {
        "id": task_id_counter,
        "text": data.get("text", "").strip(),
        "done": False,
        "created": datetime.now().strftime("%b %d, %H:%M")
    }
    if task["text"]:
        tasks.append(task)
        task_id_counter += 1
        return jsonify(task), 201
    return jsonify({"error": "Task text required"}), 400

@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return jsonify(task)
    return jsonify({"error": "Not found"}), 404

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host ="0.0.0.0",port=5019)
