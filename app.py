from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# In-memory list of tasks
tasks = [
    {"id": 1, "title": "Sample Task 1", "description": "Example description", "completed": False},
    {"id": 2, "title": "Sample Task 2", "description": "Another example task", "completed": True},
]

# Set OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_id = max(task['id'] for task in tasks) + 1 if tasks else 1
    task = {
        "id": new_id,
        "title": data.get('title'),
        "description": data.get('description'),
        "completed": False
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/ask', methods=['POST'])
def ask():
    """
    Expects JSON with a 'question' field.
    Uses OpenAI to answer questions based on the current task list.
    """
    question = request.json.get('question')
    tasks_summary = "\n".join([f"{t['id']}. {t['title']} - {t['description']} - Completed: {t['completed']}" for t in tasks])
    prompt = f"Here is a list of tasks:\n{tasks_summary}\n\nQuestion: {question}\nAnswer:"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.5,
        )
        answer = response.choices[0].text.strip()
    except Exception as e:
        answer = "Error retrieving answer from AI: " + str(e)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
