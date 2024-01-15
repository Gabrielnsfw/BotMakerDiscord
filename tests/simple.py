import os
import requests

API_KEY = os.environ.get("REPLIT_API_KEY")
BOT_PROJECT_ID = "my-bot-project"
NEW_PROJECT_NAME = "my-bot-instance"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GITHUB_REPO_URL = "https://github.com/my-username/my-bot-project.git"

def make_replit_request(method, url, data=None):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.request(method, url, headers=headers, data=data)
    return response

def create_new_project():
    response = make_replit_request(
        "POST",
        "https://api.replit.com/v1/projects",
        data={"name": NEW_PROJECT_NAME}
    )

    return response.json()["id"] if response.status_code == 201 else None

def clone_bot_project(project_id):
    response = make_replit_request(
        "POST",
        f"https://api.replit.com/v1/projects/{project_id}/clones",
        data={"url": GITHUB_REPO_URL}
    )

def replace_bot_token(project_id):
    code_response = make_replit_request(
        "GET",
        f"https://api.replit.com/v1/projects/{project_id}/files/main.py"
    )

    if code_response.status_code == 200:
        bot_code = code_response.json()["content"]
        modified_code = bot_code.replace("YOUR_PLACEHOLDER_TOKEN", BOT_TOKEN)

        update_response = make_replit_request(
            "PUT",
            f"https://api.replit.com/v1/projects/{project_id}/files/main.py",
            data={"content": modified_code}
        )

def run_bot_project(project_id):
    make_replit_request(
        "POST",
        f"https://api.replit.com/v1/projects/{project_id}/run",
        data={"command": "python3 main.py"}
    )

# Main execution
new_project_id = create_new_project()

if new_project_id:
    clone_bot_project(new_project_id)
    replace_bot_token(new_project_id)
    run_bot_project(new_project_id)
