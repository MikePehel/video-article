import os
import tempfile
from git import Repo
from urllib.parse import urlparse
import base64
from github import Github

def analyze_github_repo(repo_url):
    # Extract owner and repo name from URL
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    owner, repo_name = path_parts[0], path_parts[1]

    # Initialize GitHub API client using the token from config.py
    g = Github(os.environ.get('GITHUB_TOKEN'))
    repo = g.get_repo(f"{owner}/{repo_name}")

    all_code = ""
    
    # Try to clone the repository first
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            Repo.clone_from(repo_url, temp_dir)
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(('.py', '.js', '.html', '.css', '.java', '.cpp', '.toml', '.xml', '.json', '.jsonl')):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            all_code += f"\n\n--- {file} ---\n{f.read()}"
    except Exception as e:
        print(f"Cloning failed: {str(e)}. Falling back to API method.")
        # If cloning fails, fall back to using the GitHub API
        def get_contents(path=''):
            nonlocal all_code
            contents = repo.get_contents(path)
            for content in contents:
                if content.type == 'dir':
                    get_contents(content.path)
                elif content.name.endswith(('.py', '.js', '.html', '.css', '.java', '.cpp', '.toml', '.xml', '.json', '.jsonl')):
                    file_content = base64.b64decode(content.content).decode('utf-8')
                    all_code += f"\n\n--- {content.path} ---\n{file_content}"

        get_contents()

    # Fetch README content
    try:
        readme = repo.get_readme()
        readme_content = base64.b64decode(readme.content).decode('utf-8')
    except:
        readme_content = "README not found"
    print("All code loaded:")
    print('-----------------------------------------------------------')
    print(all_code)
    print('-----------------------------------------------------------')

    return all_code, readme_content
