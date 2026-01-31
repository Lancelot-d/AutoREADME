"""GitHub API client for repository and README operations."""
import base64
from typing import List, Optional, Dict, Any
import requests


class GitHubClient:
    """Client for interacting with GitHub API."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: str):
        """
        Initialize GitHub client.
        
        Args:
            token: GitHub personal access token for authentication.
        """
        self._token = token
        self._headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self._token}"
        }
    
    def get_public_repos(self, username: str) -> List[Dict[str, Any]]:
        """
        Get all public repositories for a given GitHub username.
        
        Args:
            username: GitHub username to fetch repositories for.
            
        Returns:
            List of repository dictionaries.
            
        Raises:
            requests.HTTPError: If the API request fails.
        """
        url = f"{self.BASE_URL}/users/{username}/repos"
        response = requests.get(url, headers=self._headers)
        response.raise_for_status()
        return response.json()
    
    def get_readme(self, owner: str, repo_name: str) -> Optional[str]:
        """
        Fetch the README content for a specific repository.
        
        Args:
            owner: Repository owner username.
            repo_name: Name of the repository.
            
        Returns:
            README content as string, or None if not found.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo_name}/readme"
        response = requests.get(url, headers=self._headers)
        
        if response.status_code == 200:
            data = response.json()
            content_encoded = data.get("content", "")
            try:
                content = base64.b64decode(content_encoded).decode("utf-8", errors="ignore")
                return content
            except Exception as e:
                print(f"Error decoding README for {repo_name}: {e}")
                return None
        return None
    
    def get_readme_metadata(self, owner: str, repo_name: str) -> Optional[Dict[str, Any]]:
        """
        Get README metadata including SHA hash.
        
        Args:
            owner: Repository owner username.
            repo_name: Name of the repository.
            
        Returns:
            README metadata dictionary, or None if not found.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo_name}/readme"
        response = requests.get(url, headers=self._headers)
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def update_readme(self, owner: str, repo_name: str, content: str, 
                     commit_message: str = "Update README.md") -> bool:
        """
        Update the README content for a specific repository.
        
        Args:
            owner: Repository owner username.
            repo_name: Name of the repository.
            content: New README content as string.
            commit_message: Commit message for the update.
            
        Returns:
            True if update was successful, False otherwise.
            
        Raises:
            requests.HTTPError: If the API request fails.
        """
        # First, get the current README metadata to obtain SHA
        readme_metadata = self.get_readme_metadata(owner, repo_name)
        
        if not readme_metadata:
            print(f"Could not find README for {repo_name}")
            return False
        
        sha = readme_metadata.get("sha")
        path = readme_metadata.get("path", "README.md")
        
        # Encode content to base64
        content_encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        
        # Update the file via GitHub API
        url = f"{self.BASE_URL}/repos/{owner}/{repo_name}/contents/{path}"
        payload = {
            "message": commit_message,
            "content": content_encoded,
            "sha": sha
        }
        
        response = requests.put(url, headers=self._headers, json=payload)
        
        if response.status_code in (200, 201):
            print(f"✅ Successfully updated README for {repo_name}")
            return True
        else:
            print(f"❌ Failed to update README for {repo_name}: {response.status_code}")
            print(f"Response: {response.text}")
            response.raise_for_status()
            return False
