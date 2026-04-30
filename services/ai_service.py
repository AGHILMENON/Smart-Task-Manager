from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL

def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)

def suggest_task_improvements(task_title: str, task_description: str = "") -> str:
    """Use Groq AI to suggest improvements for a task"""
    if not GROQ_API_KEY:
        return "AI suggestions not available - please configure GROQ_API_KEY"
    
    try:
        client = get_groq_client()
        prompt = f"""
        Given this task:
        Title: {task_title}
        Description: {task_description}
        
        Please provide 2-3 brief suggestions to make this task more actionable or effective.
        Keep suggestions concise and practical.
        """
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI suggestion error: {str(e)}"

def generate_task_from_description(description: str) -> dict:
    """Use Groq AI to generate a structured task from a natural language description"""
    if not GROQ_API_KEY:
        return {"title": description[:50], "description": description, "priority": "medium"}
    
    try:
        client = get_groq_client()
        prompt = f"""
        Convert this natural language description into a structured task:
        "{description}"
        
        Return a JSON-like structure with:
        - title: A concise title (max 50 chars)
        - description: Full description
        - priority: low/medium/high based on urgency
        - estimated_time: optional time estimate in hours
        
        Format as simple text with clear labels.
        """
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.5
        )
        
        # Parse the response (simplified parsing)
        content = response.choices[0].message.content.strip()
        return {"ai_generated": True, "suggestion": content}
    except Exception as e:
        return {"title": description[:50], "description": description, "priority": "medium", "error": str(e)}