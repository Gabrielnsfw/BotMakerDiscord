import os
import requests

class ReplitProjectManager:
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
        response = ReplitRequestHandler.make_request(
            "POST",
            "https://api.replit.com/v1/projects",
            {"name": self.new_project_name},
            headers=self._get_headers()
        )

        return ReplitResponseHandler.handle_creation_response(response, f"Project {self.new_project_name} created successfully")

    def clone_bot_project(self, project_id):
        response = ReplitRequestHandler.make_request(
            "POST",
            f"https://api.replit.com/v1/projects/{project_id}/clones",
            {"url": self.github_repo_url},
            headers=self._get_headers()
        )

        ReplitResponseHandler.handle_response(response, "Bot project cloned successfully")

    def replace_bot_token(self, project_id):
        bot_code = BotCodeModifier.get_bot_code(project_id, self.api_key)

        if bot_code:
            modified_code = BotCodeModifier.replace_token(bot_code, "YOUR_PLACEHOLDER_TOKEN", self.bot_token)

            update_response = ReplitRequestHandler.make_request(
                "PUT",
                f"https://api.replit.com/v1/projects/{project_id}/files/main.py",
                {"content": modified_code},
                headers=self._get_headers()
            )

            ReplitResponseHandler.handle_response(update_response, "Bot token replaced successfully")

    def run_bot_project(self, project_id):
        response = ReplitRequestHandler.make_request(
            "POST",
            f"https://api.replit.com/v1/projects/{project_id}/run",
            {"command": "python3 main.py"},
            headers=self._get_headers()
        )

        ReplitResponseHandler.handle_response(response, "Bot project running successfully")

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.api_key}"}

class ReplitRequestHandler:
    @staticmethod
    def make_request(method, url, data=None, headers=None):
        response = requests.request(method, url, headers=headers, data=data)
        return response

class ReplitResponseHandler:
    @staticmethod
    def handle_creation_response(response, success_message):
        if response.status_code == 200 or response.status_code == 201:
            print(success_message)
            return response.json()["id"]
        else:
            print(f"Error: {response.text}")
            return None

    @staticmethod
    def handle_response(response, success_message):
        if response.status_code == 200 or response.status_code == 201:
            print(success_message)
        else:
            print(f"Error: {response.text}")

class BotCodeModifier:
    @staticmethod
    def get_bot_code(project_id, api_key):
        response = ReplitRequestHandler.make_request(
            "GET",
            f"https://api.replit.com/v1/projects/{project_id}/files/main.py",
            headers={"Authorization": f"Bearer {api_key}"}
        )

        if response.status_code == 200:
            return response.json()["content"]
        else:
            print(f"Error retrieving bot code: {response.text}")
            return None

    @staticmethod
    def replace_token(code, placeholder, new_token):
        return code.replace(placeholder, new_token)

# Replace with your actual values
api_key = os.environ.get("REPLIT_API_KEY")
bot_project_id = "my-bot-project"
new_project_name = "my-bot-instance"
bot_token = os.environ.get("BOT_TOKEN")
github_repo_url = "https://github.com/my-username/my-bot-project.git"

project_manager = ReplitProjectManager(api_key, bot_project_id, new_project_name, bot_token, github_repo_url)
project_manager.create_and_run_bot()
