import os
from pathlib import Path
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from dotenv import load_dotenv

load_dotenv()

# 1. Define the Loader
def load_frontend_instructions():
    """Only loads the files essential for Frontend Development to save tokens."""
    essential_files = [
        "Prompts/design/design-ux-architect.md", 
        "Prompts/design/design-ui-designer.md",   
        "Prompts/engineering/engineering-frontend.md"
    ]
    
    # We add a specific instruction here to force the AI to use the tool
    combined_prompt = "# FRONTEND SPECIALIST CONTEXT\n"
    combined_prompt += "IMPORTANT: Use the 'save_code_to_disk' tool to save all code outputs to the specified path.\n\n"
    
    for file_path in essential_files:
        path = Path(file_path)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                agent_role = path.stem.replace('-', ' ').title()
                combined_prompt += f"## {agent_role} Rules\n{f.read()}\n\n---\n\n"
    return combined_prompt

# 2. Define the Tool Function First
def save_code_to_disk(ctx: RunContext[None], filename: str, content: str) -> str:
    """
    Saves code content to a file on the local disk.
    Args:
        filename: The name of the file with extension.
        content: The actual code string to be saved.
    """
    try:
        # Using your specific project path
        file_path = Path(r"D:\Prototype_agent\tic-tac-toe") / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Successfully saved to {file_path}. You can run it now."
    except Exception as e:
        return f"Error saving file: {str(e)}"

# 3. Initialize Model and Agent LAST
model = GroqModel(
    'openai/gpt-oss-120b',
    provider=GroqProvider(api_key=os.getenv('GROQ_API_KEY'))
)

agent = Agent(
    model, 
    system_prompt=load_frontend_instructions(),
    tools=[save_code_to_disk] # Correctly defined now
)

# 4. Interactive Loop
if __name__ == "__main__":
    while True:
        user_input = input("Enter your prompt (or 'exit'): ")
        if user_input.lower() == "exit":
            break
        
        # Pydantic AI will now trigger save_code_to_disk automatically when needed
        response = agent.run_sync(user_input)
        print(response.output)