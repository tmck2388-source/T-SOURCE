"""
Code Assistant
AI-powered code generation, fixing, and learning with semi-autonomous capabilities
"""
from typing import Optional, List, Dict
import json
import subprocess
import os
from pathlib import Path

class CodeAssistant:
    """Assist with code generation, debugging, and execution"""
    
    def __init__(self, ai_client, web_search_engine):
        self.ai_client = ai_client
        self.web_search = web_search_engine
        self.code_history = []
        self.learned_patterns = {}
    
    def generate_code(
        self,
        description: str,
        language: str = "python",
        framework: Optional[str] = None
    ) -> str:
        """
        Generate code based on description
        
        Args:
            description: What the code should do
            language: Programming language
            framework: Optional framework (django, flask, etc)
        
        Returns:
            Generated code
        """
        
        prompt = f"""Generate {language} code that does the following:
{description}

"""
        if framework:
            prompt += f"Framework: {framework}\n"
        
        prompt += """Requirements:
- Clean, well-commented code
- Best practices for the language
- Error handling
- Type hints (if applicable)
- Follow modern conventions
- Production-ready quality
"""
        
        code = self.ai_client.generate(prompt)
        
        self.code_history.append({
            "description": description,
            "language": language,
            "framework": framework,
            "code": code
        })
        
        return code
    
    def fix_code(self, code: str, error: str, language: str = "python") -> str:
        """
        Fix broken code based on error message
        
        Args:
            code: The broken code
            error: Error message or description
            language: Programming language
        
        Returns:
            Fixed code
        """
        
        prompt = f"""Fix the following {language} code that has this error:
{error}

Broken code:
```{language}
{code}
```

Provide:
1. The corrected code
2. Brief explanation of the fix
3. How to prevent this error in future

Use the same language and style as the original.
"""
        
        fixed = self.ai_client.generate(prompt)
        return fixed
    
    def learn_and_apply(self, code_snippet: str, language: str = "python") -> Dict:
        """
        Learn from a code snippet and store patterns
        
        Args:
            code_snippet: Code to learn from
            language: Programming language
        
        Returns:
            Pattern analysis
        """
        
        prompt = f"""Analyze this {language} code and extract key patterns:
```{language}
{code_snippet}
```

Identify:
1. Design patterns used
2. Best practices applied
3. Potential improvements
4. Reusable components
"""
        
        analysis = self.ai_client.generate(prompt)
        
        self.learned_patterns[hash(code_snippet)] = {
            "snippet": code_snippet,
            "language": language,
            "analysis": analysis
        }
        
        return {"analysis": analysis}
    
    def execute_code_safe(
        self,
        code: str,
        language: str = "python",
        timeout: int = 10
    ) -> Dict:
        """
        Safely execute code in isolated environment
        
        Args:
            code: Code to execute
            language: Programming language
            timeout: Execution timeout in seconds
        
        Returns:
            Execution result
        """
        
        try:
            if language == "python":
                # Create temporary file
                temp_file = Path("/tmp/otta_exec.py")
                temp_file.write_text(code)
                
                result = subprocess.run(
                    ["python", str(temp_file)],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                temp_file.unlink()
                
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr,
                    "return_code": result.returncode
                }
            else:
                return {
                    "success": False,
                    "error": f"Execution for {language} not yet implemented"
                }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Code execution timed out after {timeout} seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def semi_autonomous_build(
        self,
        project_spec: str,
        language: str = "python"
    ) -> Dict:
        """
        Semi-autonomously build a project from specification
        
        Args:
            project_spec: Description of what to build
            language: Programming language
        
        Returns:
            Project info and generated files
        """
        
        # Search for latest practices
        search_results = self.web_search.search(
            f"best practices {language} {project_spec} 2024",
            max_results=3
        )
        
        context = "Recent best practices found:\n"
        for result in search_results:
            context += f"- {result['title']}\n"
        
        prompt = f"""Build a complete {language} project based on this specification:
{project_spec}

{context}

Create:
1. Project structure (folder layout)
2. Main application files
3. Configuration files
4. Dependencies/requirements
5. Simple setup instructions

Incorporate the latest best practices from the search results.
Output as structured JSON with file paths and contents.
"""
        
        response = self.ai_client.generate(prompt)
        
        return {
            "spec": project_spec,
            "language": language,
            "project_structure": response
        }

# Example usage
def demo_code_assistance(ai_client, web_search):
    assistant = CodeAssistant(ai_client, web_search)
    
    # Generate code example
    code = assistant.generate_code(
        "Create a simple web scraper that fetches titles from a website",
        language="python",
        framework="requests"
    )
    
    print("Generated Code:")
    print(code)
    
    return assistant