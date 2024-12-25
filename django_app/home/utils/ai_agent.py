from groq import Groq

key = "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"

#Anlyze the given code(fetched) using LLM model from Groq
def analyze_code_with_llm(file_content, file_name):
    prompt = f"""
    Analyze the following code for:
    - Code style and formatting issues
    - Potential bugs or errors
    - Performance improvements
    - Best practices

    File: {file_name}
    Content: {file_content}

    Provide a detailed JSON output with the following structure:
    {{
        "Issues": 
        [
            {{
                "type": "<style|bug|performance|best_practice>",
                "line": <line_number>,
                "description": "<description>",
                "suggestion": "<suggestion>"
            }}
        ]
    }}
    ```json
    """

    client = Groq(
        api_key= key
    )
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=
        [
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
    print(completion.choices[0].message.content)
    result_content = ""
    # for chunk in completion:
    #     result_content += chunk.choices[0].delta.content or ""
    return completion.choices[0].message.content

