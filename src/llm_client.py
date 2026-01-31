"""LLM client for interacting with Together AI API."""
from together import Together


class LLMClient:
    """Client for interacting with Together AI's LLM API."""
    
    DEFAULT_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    
    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        """
        Initialize LLM client.
        
        Args:
            api_key: Together AI API key for authentication.
            model: Model identifier to use for completions.
        """
        self._client = Together(api_key=api_key)
        self._model = model
    
    def generate_completion(self, prompt: str) -> str:
        """
        Generate a completion from the LLM for the given prompt.
        
        Args:
            prompt: The prompt to send to the LLM.
            
        Returns:
            The generated completion text.
            
        Raises:
            Exception: If the API call fails.
        """
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content
    
    

    def generate_readme_profile_section(self, projects: list[dict]) -> str:
        """
        Generate a README profile section with multiple projects.
        
        Args:
            projects: List of project dictionaries, each containing:
                - 'name': Project name
                - 'description': One-liner description
                - 'url': Link to the project
            
        Returns:
            Generated README profile section in Markdown format.
        """
        
        projects_text = "\n".join([
            f"- {project['name']}: {project['description']} ({project['url']})"
            for project in projects
        ])
        
        prompt = f"""Generate a professional and engaging README profile section that includes:
        - A brief introduction be professional and engaging but concise and not too much, that include that I am a software developer loving automation.
        - A showcase of the following projects in a three-liner format (Brief description and skill used and link):
        {projects_text}

        My contact information is  : https://www.linkedin.com/in/lancelot-domart-83b762204/
        
        Format the output in clean Markdown with appropriate headers, emojis, and styling.
        Make it concise and visually appealing for a GitHub profile README.
        """
        
        return self.generate_completion(prompt)
