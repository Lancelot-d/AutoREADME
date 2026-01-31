"""Main application entry point for AutoREADME."""
from config import Config
from github_client import GitHubClient
from llm_client import LLMClient


class AutoREADMEApp:
    """Main application class for managing README operations."""
    
    def __init__(self, config: Config):
        """
        Initialize the application.
        
        Args:
            config: Application configuration instance.
        """
        self.config = config
        self.github_client = GitHubClient(token=config.github_token)
        self.llm_client = LLMClient(api_key=config.together_api_key)
        self.ban_repos = ["Lancelot-d"]  # Repositories to exclude from processing
    
    def generate_profile_readme(self) -> str:
        """
        Generate a GitHub profile README section based on user's repositories.
        
        Returns:
            Generated README profile section in Markdown format.
        """
        try:
            repos = self.github_client.get_public_repos(self.config.github_username)
            
            # Filter out banned repositories
            repos = [repo for repo in repos if repo["name"].lower() not in [r.lower() for r in self.ban_repos]]
            
            # Format repositories into the required structure
            projects = [
                {
                    "name": repo["name"],
                    "description": repo.get("description") or "A GitHub project",
                    "url": repo["html_url"]
                }
                for repo in repos
            ]
            
            # Generate the profile README section using LLM
            profile_section = self.llm_client.generate_readme_profile_section(projects)
            
            print("\n" + "="*60)
            print("Generated Profile README Section:")
            print("="*60)
            print(profile_section)
            print("="*60 + "\n")
            
            return profile_section
            
        except Exception as e:
            print(f"Error generating profile README: {e}")
            return ""
    
    def update_repository_readme(self, repo_name: str, new_content: str, 
                                 commit_message: str = "Update README via AutoREADME") -> bool:
        """
        Update the README for a specific repository.
        
        Args:
            repo_name: Name of the repository to update.
            new_content: New README content.
            commit_message: Commit message for the update.
            
        Returns:
            True if update was successful, False otherwise.
        """
        try:
            success = self.github_client.update_readme(
                owner=self.config.github_username,
                repo_name=repo_name,
                content=new_content,
                commit_message=commit_message
            )
            return success
        except Exception as e:
            print(f"Error updating README for {repo_name}: {e}")
            return False
    
    def run(self) -> None:
        """Execute the main application flow."""
        
        profile_content = self.generate_profile_readme()
        # Update the profile README (username/username repository)
        if profile_content:
            self.update_repository_readme(
                repo_name=self.config.github_username,
                new_content=profile_content,
                commit_message="Update profile README via AutoREADME"
            )
        


def main():
    """Application entry point."""
    try:
        config = Config.from_env()
        app = AutoREADMEApp(config)
        app.run()
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
