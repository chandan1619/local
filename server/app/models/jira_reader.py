import requests
from llama_index.core.schema import Document


class JiraDataLoader:
    def __init__(self, api_token):
        self.api_token = api_token
        self.user_info = self.get_user_info()
        self.email = self.user_info.get('emailAddress') if self.user_info else None
        self.base_url = f'https://{self.user_info["domain"]}.atlassian.net/rest/api/3' if self.user_info and "domain" in self.user_info else None
        self.auth = (self.email, self.api_token) if self.email else None

    def get_user_info(self):
        """Fetches user details to infer email and domain; modify the domain logic as per actual API response capability."""
        # This URL needs to be adjusted based on the actual API that can give you user details
        url = 'https://api.atlassian.com/me'
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            # Assuming domain can be extracted or inferred here, often it's not possible directly
            user_data['domain'] = user_data['account_id'].split('-')[0]  # Example, adjust based on actual data
            return user_data
        else:
            print(f"{response.json()=}")
            raise Exception("Failed to fetch user information from API Token")

    def get_projects(self):
        """Fetches all projects from Jira."""
        if not self.auth:
            raise Exception("Authentication details not set up correctly")
        url = f'{self.base_url}/project'
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"{response.json()=}")
            raise Exception("Failed to fetch projects")

    def get_issues_for_project(self, project_id):
        """Fetches all issues for a given project."""
        url = f'{self.base_url}/search?jql=project={project_id}'
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            return response.json()['issues']
        else:
            raise Exception(f"Failed to fetch issues for project {project_id}")

    def load_data(self):
        """Compiles data of all projects and their issues into Document array."""
        documents = []
        projects = self.get_projects()

        for project in projects:
            project_id = project['id']
            project_name = project['name']
            issues = self.get_issues_for_project(project_id)
            for issue in issues:
                issue_key = issue['key']
                issue_summary = issue['fields']['summary']
                issue_status = issue['fields']['status']['name']
                text_content = f"Project: {project_name} (ID: {project_id}), Issue: {issue_key}, Summary: {issue_summary}, Status: {issue_status}"
                documents.append(Document(text=text_content))

        return documents
