from openai import OpenAI
import json

client = OpenAI(api_key="YOUR_API_KEY")

TASK_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def ai_agent(user_message):
    tasks = load_tasks()

    prompt = f"""
You are a Smart Task Assistant AI.

User said: {user_message}

Current Tasks: {tasks}

If user asks to add a task → respond: ADD|task-name  
If user asks to delete a task → respond: DELETE|task-name  
If user asks to list tasks → respond: LIST  
If user asks for summary → respond: SUMMARY|text  
If user asks for motivation → respond: MOTIVATION
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def run_agent(message):
    output = ai_agent(message)

    if output.startswith("ADD"):
        task = output.split("|")[1]
        tasks = load_tasks()
        tasks.append(task)
        save_tasks(tasks)
        return f"Added task: {task}"

    elif output.startswith("LIST"):
        tasks = load_tasks()
        return f"Your Tasks:\n" + "\n".join(tasks)

    elif output.startswith("DELETE"):
        task = output.split("|")[1]
        tasks = load_tasks()
        if task in tasks:
            tasks.remove(task)
            save_tasks(tasks)
            return f"Deleted task: {task}"
        return "Task not found."

    elif output.startswith("SUMMARY"):
        text = output.split("|")[1]
        return client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"Summarize: {text}"}
            ]
        ).choices[0].message.content

    elif output.startswith("MOTIVATION"):
        return "You are stronger than your doubts — keep moving, future software engineer!"

    return "Sorry, I didn't understand."

# Example
print(run_agent("Add task: Study Python"))
print(run_agent("Show my tasks"))