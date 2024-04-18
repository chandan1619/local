import requests
from llama_index.core.schema import Document


class GitHubDataLoader:
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

    def get_commits(self, repo_name, branch_name):
        """Fetches commits for a given repository and branch."""
        url = f'https://api.github.com/repos/{self.username}/{repo_name}/commits?sha={branch_name}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            commits = response.json()
            return [f"Commit: {commit['commit']['message']} by {commit['commit']['author']['name']} on {commit['commit']['author']['date']}" for commit in commits]
        else:
            raise Exception(f"Failed to fetch commits for repository {repo_name} on branch {branch_name}")

    def get_issues(self, repo_name):
        """Fetches issues for a given repository."""
        url = f'https://api.github.com/repos/{self.username}/{repo_name}/issues'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            issues = response.json()
            return [f"Issue: {issue['title']}, Status: {issue['state']}, Raised by: {issue['user']['login']}" for issue in issues]
        else:
            raise Exception(f"Failed to fetch issues for repository {repo_name}")


    def load_data(self):
        """Compiles text data of all repositories, their branches, and commit details into Document array."""
        documents = []
        repos = self.get_repos()

        for repo in repos:
            repo_name = repo['name']
            branches = self.get_branches(repo_name)
            for branch in branches:
                commits = self.get_commits(repo_name, branch)
                issues = self.get_issues(repo_name)
                # Construct a text with all commit details
                text_content = f"""{{github repository name: {repo_name}, Banrch name: {branch},Branch commits : {commits}. issues : {issues}}}"""
                documents.append(Document(text=text_content, metadata={"github repository name":repo_name ,"Branch name" : branch, "source": "github"}))

        return documents
