from flask import request, jsonify, Flask
    

app = Flask(__name__) # Cria uma instância do Flask

tasks = []  # Lista para armazenar as tarefas
task_id_control = 1  # Controlador de IDs para garantir unicidade

@app.route("/") # Rota para a página inicial
def hello():
    return "Hello, World!"

@app.route("/tasks", methods=["POST"])
def create_task(): # Função para criar uma nova tarefa
    global task_id_control
    data = request.get_json()
    new_task = {
        "id": task_id_control, # ID único da tarefa
        "title": data.get("title"),  # Obtém o título enviado
        "description": data.get("description", ""),  # Descrição opcional
        "completed": False  # Define que a tarefa começa como incompleta
    }
    tasks.append(new_task)  # Adiciona a nova tarefa à lista
    task_id_control += 1
    return jsonify({"message": "Tarefa criada com sucesso!", "task": new_task}), 201
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks, "total": len(tasks)})

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id): # tarefa por ID
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    return jsonify(task) # Retorna a tarefa encontrada
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    data = request.get_json()
    # Atualiza os campos da tarefa com os dados enviados
    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    task["completed"] = data.get("completed", task["completed"])
    return jsonify({"message": "Tarefa atualizada com sucesso!", "task": task})

@app.route("/tasks/<int:task_id>", methods=["DELETE"]) # Metodo de deletar tarefas
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Tarefa deletada com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True)  # Inicia o servidor em modo de depuração