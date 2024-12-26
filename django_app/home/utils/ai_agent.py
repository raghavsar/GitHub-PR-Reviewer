# ai_agent.py
from groq import Groq
from .prompts import system_prompt
import json

def analyze_code_with_llm(file_content, file_name):
    """Analyzes the given code using an LLM."""
    prompt = f"""
    Analyze the following code for:
    - Code style and formatting issues
    - Potential bugs or errors
    - Performance improvements
    - Best practices

    File: {file_name}
    Content:
    {file_content}

    Provide a detailed JSON output with the structure:
    {{
        "issues": [
            {{
                "type": "<style|bug|performance|best_practice>",
                "line": <line_number>,
                "description": "<description>",
                "suggestion": "<suggestion>"
            }}
        ]
    }}
    ``json
    """

    client = Groq(
        api_key="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"
    )
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {'role': 'system', 'content': system_prompt},
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        top_p=1,
        response_format={
            "type": "json_object"
        },
    )
    return completion.choices[0].message.content