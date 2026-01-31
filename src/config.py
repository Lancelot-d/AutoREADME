"""Configuration module for managing environment variables and settings."""
import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration class."""
    
    github_username: str
    github_token: str
    together_api_key: str
    
    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.
        
        Returns:
            Config: Configuration instance with loaded values.
            
        Raises:
            ValueError: If required environment variables are missing.
        """
        load_dotenv()
        
        github_token = os.getenv("GH_TOKEN")
        together_api_key = os.getenv("TOGETHER_API_KEY")
        github_username = "lancelot-d"  # Fixed username for the application
        
        if not github_token:
            raise ValueError("GH_TOKEN environment variable is required")
        if not together_api_key:
            raise ValueError("TOGETHER_API_KEY environment variable is required")
        
        return cls(
            github_username=github_username,
            github_token=github_token,
            together_api_key=together_api_key
        )
