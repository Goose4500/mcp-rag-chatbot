"""
fetch_docs.py - Script to fetch Model Context Protocol (MCP) documentation from GitHub
"""

import os
import base64
from github import Github
import requests
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables (for GitHub token)
load_dotenv()

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Set your GitHub token in .env file
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
REPOS = [
    ('modelcontextprotocol', 'docs'),        # Documentation
    ('modelcontextprotocol', 'specification'),  # Specification
    ('modelcontextprotocol', 'python-sdk'),  # Python SDK
    ('modelcontextprotocol', 'typescript-sdk')  # TypeScript SDK
]

def ensure_dir(directory):
    """Ensure directory exists"""
    os.makedirs(directory, exist_ok=True)

def download_file(url, token, output_path):
    """Download a file from GitHub API"""
    headers = {'Authorization': f'token {token}'} if token else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = base64.b64decode(response.json().get('content', ''))
        with open(output_path, 'wb') as f:
            f.write(content)
        return True
    else:
        logger.error(f"Failed to download {url}: {response.status_code}")
        return False

def process_contents(repo, path, output_dir, token):
    """Process contents of a repository recursively"""
    headers = {'Authorization': f'token {token}'} if token else {}
    api_url = f"https://api.github.com/repos/{repo[0]}/{repo[1]}/contents/{path}"
    
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        logger.error(f"Failed to access {api_url}: {response.status_code}")
        return
    
    contents = response.json()
    
    # Handle list of files/directories
    if isinstance(contents, list):
        for item in contents:
            item_path = item['path']
            item_name = os.path.basename(item_path)
            item_type = item['type']
            
            # Create subdirectory for this path
            subdir = os.path.join(output_dir, path) if path else output_dir
            ensure_dir(subdir)
            
            if item_type == 'dir':
                # Recursively process subdirectories
                process_contents(repo, item_path, output_dir, token)
            elif item_type == 'file':
                # Only download markdown and text files
                if item_name.endswith(('.md', '.txt', '.json')):
                    output_path = os.path.join(subdir, item_name)
                    download_file(item['download_url'], token, output_path)
                    logger.info(f"Downloaded {item_path}")
    
    # Handle single file
    elif isinstance(contents, dict) and contents.get('type') == 'file':
        file_name = os.path.basename(contents['path'])
        if file_name.endswith(('.md', '.txt', '.json')):
            output_path = os.path.join(output_dir, file_name)
            download_file(contents['download_url'], token, output_path)
            logger.info(f"Downloaded {contents['path']}")

def fetch_documentation():
    """Main function to fetch all MCP documentation"""
    logger.info("Starting documentation fetch...")
    
    # Create data directory if it doesn't exist
    ensure_dir(DATA_DIR)
    
    # Process each repository
    for repo in REPOS:
        repo_dir = os.path.join(DATA_DIR, repo[1])
        ensure_dir(repo_dir)
        logger.info(f"Processing repository: {repo[0]}/{repo[1]}")
        process_contents(repo, "", repo_dir, GITHUB_TOKEN)
    
    logger.info("Documentation fetch completed.")

if __name__ == "__main__":
    fetch_documentation()