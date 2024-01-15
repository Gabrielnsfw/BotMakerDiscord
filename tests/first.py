import os
import requests

API_KEY = os.environ.get("REPLIT_API_KEY")
BOT_PROJECT_ID = "my-bot-project"
NEW_PROJECT_NAME = "my-bot-instance"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GITHUB_REPO_URL = "https://github.com/my-username/my-bot-project.git"

def create_new_project():
    response = requests.post(
        "https://api.replit.com/v1/projects",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data={"name": NEW_PROJECT_NAME}
    )

    return handle_response(response, f"Project {NEW_PROJECT_NAME} created successfully")

def clone_bot_project(project_id):
    response = requests.post(
        f"https://api.replit.com/v1/projects/{project_id}/clones",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data={"url": GITHUB_REPO_URL}
    )

    return handle_response(response, "Bot project cloned successfully")

def replace_bot_token(project_id):
    response = requests.get(
        f"https://api.replit.com/v1/projects/{project_id}/files/main.py",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )

    if response.status_code == 200:
        bot_code = response.json()["content"]
        modified_code = bot_code.replace("YOUR_PLACEHOLDER_TOKEN", BOT_TOKEN)

        update_response = requests.put(
            f"https://api.replit.com/v1/projects/{project_id}/files/main.py",
            headers={"Authorization": f"Bearer {API_KEY}"},
            data={"content": modified_code}
        )

        return handle_response(update_response, "Bot token replaced successfully")

    else:
        print(f"Error retrieving bot code: {response.text}")
        return None

def run_bot_project(project_id):
    response = requests.post(
        f"https://api.replit.com/v1/projects/{project_id}/run",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data={"command": "python3 main.py"}
    )

    return handle_response(response, "Bot project running successfully")

def handle_response(response, success_message):
    if response.status_code == 200 or response.status_code == 201:
        print(success_message)
        return response.json()["id"]
    else:
        print(f"Error: {response.text}")
        return None

new_project_id = create_new_project()

if new_project_id:
    clone_bot_project(new_project_id)
    replace_bot_token(new_project_id)
    run_bot_project(new_project_id)
