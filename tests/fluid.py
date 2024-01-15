import os
import requests

class ReplitBotManager:
    def __init__(self, api_key, bot_project_id, new_project_name, bot_token, github_repo_url):
        self.api_key = api_key
        self.bot_project_id = bot_project_id
        self.new_project_name = new_project_name
        self.bot_token = bot_token
        self.github_repo_url = github_repo_url

    def create_and_run_bot(self):
        new_project_id = self.create_new_project()
        
        if new_project_id:
            self.clone_bot_project(new_project_id)
            self.replace_bot_token(new_project_id)
            self.run_bot_project(new_project_id)

    def create_new_project(self):
        response = self._make_replit_request(
            "POST",
            "https://api.replit.com/v1/projects",
            {"name": self.new_project_name}
        )

        return self._handle_response(response, f"Project {self.new_project_name} created successfully")

    def clone_bot_project(self, project_id):
        response = self._make_replit_request(
            "POST",
            f"https://api.replit.com/v1/projects/{project_id}/clones",
            {"url": self.github_repo_url}
        )

        self._handle_response(response, "Bot project cloned successfully")

    def replace_bot_token(self, project_id):
        bot_code = self._get_bot_code(project_id)

        if bot_code:
            modified_code = bot_code.replace("YOUR_PLACEHOLDER_TOKEN", self.bot_token)

            update_response = self._make_replit_request(
                "PUT",
                f"https://api.replit.com/v1/projects/{project_id}/files/main.py",
                {"content": modified_code}
            )

            self._handle_response(update_response, "Bot token replaced successfully")

    def run_bot_project(self, project_id):
        response = self._make_replit_request(
            "POST",
            f"https://api.replit.com/v1/projects/{project_id}/run",
            {"command": "python3 main.py"}
        )

        self._handle_response(response, "Bot project running successfully")

    def _get_bot_code(self, project_id):
        response = self._make_replit_request(
            "GET",
            f"https://api.replit.com/v1/projects/{project_id}/files/main.py"
        )

        if response.status_code == 200:
            return response.json()["content"]
        else:
            print(f"Error retrieving bot code: {response.text}")
            return None

    def _make_replit_request(self, method, url, data=None):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.request(method, url, headers=headers, data=data)
        return response

    @staticmethod
    def _handle_response(response, success_message):
        if response.status_code == 200 or response.status_code == 201:
            print(success_message)
        else:
            print(f"Error: {response.text}")

# Replace with your actual values
api_key = os.environ.get("REPLIT_API_KEY")
bot_project_id = "my-bot-project"
new_project_name = "my-bot-instance"
bot_token = os.environ.get("BOT_TOKEN")
github_repo_url = "https://github.com/my-username/my-bot-project.git"

bot_manager = ReplitBotManager(api_key, bot_project_id, new_project_name, bot_token, github_repo_url)
bot_manager.create_and_run_bot()
