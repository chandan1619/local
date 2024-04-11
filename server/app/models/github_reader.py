import requests
from llama_index.core.schema import Document

class GitHubDataLoader:
    """_summary_
    """
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
        }
        self.username = self.get_username()

    def get_username(self):
        """Fetches the GitHub username of the authenticated user."""
        url = 'https://api.github.com/user'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get('login')
        else:
            raise Exception("Failed to fetch user information")

    def get_repos(self):
        """Fetches repositories for the authenticated user."""
        url = f'https://api.github.com/users/{self.username}/repos'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch repositories for user {self.username}")

    def get_branches(self, repo_name):
        """Fetches branches for a given repository."""
        url = f'https://api.github.com/repos/{self.username}/{repo_name}/branches'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return [branch['name'] for branch in response.json()]
        else:
            raise Exception(f"Failed to fetch branches for repository {repo_name}")

    def load_data(self):
        """Compiles text data of all repositories and their branches into Document array."""
        documents = []
        repos = self.get_repos()

        for repo in repos:
            repo_name = repo['name']
            branches = self.get_branches(repo_name)
            for branch in branches:
                # Assuming you want the repo name and branch name in the text
                text_content = f"Repository: {repo_name}, Branch: {branch}"
                documents.append(Document(text=text_content))

        return documents