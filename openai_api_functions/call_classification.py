import openai
import json
openai_key="insertyourkeyhere"
openai.api_key= openai_key

functions = [
    {
        "name": "classify_call_category",
        "description": "Summarise the transcript first and then classify the summary into a category.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["Emergency Job booked", "Regular Job booked", "Cancel Service", "Note a message", "Other"],
                    "description": "The category that best describes the call.",
                },
            },
            "required": ["category"],
        },
    }
]

def classify_call_via_openai(transcript: str) -> str:
    """
    Calls the OpenAI API to classify the call transcript using function calling.
    """
    try:
        response =  openai.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are an assistant who classifies call transcripts between an AI agent and a customer who has called to inqury at a plumbing company."},
                {"role": "user", "content": f"Classify this call transcript: {transcript}"}
            ],
            functions=functions,
            function_call={"name": "classify_call_category"}
        )

        category= json.loads(response.choices[0].message.function_call.arguments)
        return category['category']
    
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return "Other"

