import os
import requests

class ReplitProject:
    def __init__(self, api_key, bot_project_id, new_project_name, bot_token, github_repo_url):
        self.api_key = api_key
        self.bot_project_id = bot_project_id
        self.new_project_name = new_project_name
        self.bot_token = bot_token
        self.github_repo_url = github_repo_url

    def create_new_project(self):
        response = requests.post(
            "https://api.replit.com/v1/projects",
            headers={"Authorization": f"Bearer {self.api_key}"},
            data={"name": self.new_project_name}
        )

        return self.handle_response(response, f"Project {self.new_project_name} created successfully")

    def clone_bot_project(self, project_id):
        response = requests.post(
            f"https://api.replit.com/v1/projects/{project_id}/clones",
            headers={"Authorization": f"Bearer {self.api_key}"},
            data={"url": self.github_repo_url}
        )

        return self.handle_response(response, "Bot project cloned successfully")

    def replace_bot_token(self, project_id):
        response = requests.get(
            f"https://api.replit.com/v1/projects/{project_id}/files/main.py",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )

        if response.status_code == 200:
            bot_code = response.json()["content"]
            modified_code = bot_code.replace("YOUR_PLACEHOLDER_TOKEN", self.bot_token)

            update_response = requests.put(
                f"https://api.replit.com/v1/projects/{project_id}/files/main.py",
                headers={"Authorization": f"Bearer {self.api_key}"},
                data={"content": modified_code}
            )

            return self.handle_response(update_response, "Bot token replaced successfully")

        else:
            print(f"Error retrieving bot code: {response.text}")
            return None

    def run_bot_project(self, project_id):
        response = requests.post(
            f"https://api.replit.com/v1/projects/{project_id}/run",
            headers={"Authorization": f"Bearer {self.api_key}"},
            data={"command": "python3 main.py"}
        )

        return self.handle_response(response, "Bot project running successfully")

    @staticmethod
    def handle_response(response, success_message):
        if response.status_code == 200 or response.status_code == 201:
            print(success_message)
            return response.json()["id"]
        else:
            print(f"Error: {response.text}")
            return None

# Replace with your actual values
api_key = os.environ.get("REPLIT_API_KEY")
bot_project_id = "my-bot-project"
new_project_name = "my-bot-instance"
bot_token = os.environ.get("BOT_TOKEN")
github_repo_url = "https://github.com/my-username/my-bot-project.git"

replit_project = ReplitProject(api_key, bot_project_id, new_project_name, bot_token, github_repo_url)

new_project_id = replit_project.create_new_project()

if new_project_id:
    replit_project.clone_bot_project(new_project_id)
    replit_project.replace_bot_token(new_project_id)
    replit_project.run_bot_project(new_project_id)
