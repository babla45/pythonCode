# GitHub Repository Downloader and Updater Script
# -----------------------------------------------
# This script downloads all repositories from a given GitHub profile and saves them to a folder.
# If the repositories are already downloaded, the script will update them by pulling the latest changes.
#
# Requirements:
# - Python 3.x
# - Git installed and available in the system's PATH
# - Python packages: `requests`
#
# Installation:
# 1. Install Python 3.x from https://www.python.org/
# 2. Install Git from https://git-scm.com/
# 3. Install required Python packages:
#    pip install requests
#
# Usage:
# 1. Run the script:
#    python github_repo_downloader.py
# 2. Input the GitHub profile URL when prompted (e.g., https://github.com/octocat)
#
# The script will download or update the repositories to a folder named `github_repos_of_<username>`.

import requests
import subprocess
import os
import sys
import time

def get_github_username(github_url):
    # """Extract GitHub username from the provided URL."""
    if github_url.startswith("https://github.com/"):
        return github_url.split("https://github.com/")[1].split('/')[0]
    else:
        print("Invalid GitHub URL format. It should start with 'https://github.com/'")
        sys.exit(1)

def get_all_repos(username):
    # """Fetch all repositories for a given GitHub username using the GitHub API."""
    api_url = f"https://api.github.com/users/{username}/repos"
    # list of dictionaries
    repos = []
    page = 1
    
    while True:
        response = requests.get(f"{api_url}?page={page}&per_page=100")
        
        if response.status_code != 200:
            print(f"Error: Unable to fetch repositories (Status Code: {response.status_code})")
            sys.exit(1)
        
        page_repos = response.json()
        if not page_repos:
            break  # No more repositories, exit the loop
        repos.extend(page_repos)
        page += 1
    
    return repos

def clone_or_update_repos(repos, github_username):
    # """Clone new repositories or update existing ones."""
    folder_name = f"github_repos_of_{github_username}"
    os.makedirs(folder_name, exist_ok=True)

    for repo in repos:
        repo_name = repo['name']
        repo_url = repo['clone_url']
        repo_path = os.path.join(folder_name, repo_name)
        
        if os.path.exists(repo_path):
            print(f"\n\n\nUpdating repository: {repo_name}")
            # Update the repository if it already exists
            subprocess.run(['git', 'pull'], cwd=repo_path, check=True)
        else:
            print(f"\n\n\nCloning repository: {repo_name}")
            # Clone the repository if it doesn't exist
            subprocess.run(['git', 'clone', repo_url], cwd=folder_name, check=True)

def main():
    # """Main function to manage the GitHub repo cloning or updating."""
    github_url = input("Enter the GitHub profile URL (e.g., https://github.com/username): ").strip()
    github_username = get_github_username(github_url)
    
    # Fetch all repositories for the given username
    repos = get_all_repos(github_username)
    
    if not repos:
        print("No repositories found for this user.")
        sys.exit(0)
    
    print(f"\n\nFound {len(repos)} repositories. Starting download or update...")
    
    # Clone or update repositories
    clone_or_update_repos(repos, github_username)
    
    print("\n\n************** All repositories cloned/updated successfully. **************\n\n\n")

if __name__ == "__main__":
    main()
    time.sleep(3)
