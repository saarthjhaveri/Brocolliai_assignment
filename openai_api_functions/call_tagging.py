import openai
import json
openai_key="insertyourkeyhere"
openai.api_key= openai_key


functions = [
    {
        "name": "tag_call_category",
        "description": "Tag the call transcript based on the classification and flagging outputs.",
        "parameters": {
            "type": "object",
            "properties": {
                "tag": {
                    "type": "string",
                    "enum": ["Job booked", "Spam", "Estimate required", "Empty call", "Callback required"],
                    "description": "The tag that best describes the call outcome.",
                },
            },
            "required": ["tag"],
        },
    }
]

def tag_call_via_openai(transcript: str) -> str:
    """
    Calls the OpenAI API to tag the call transcript using function calling
    """
    try:
        response =  openai.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are an assistant who classifies call transcripts between an AI agent and a customer who has called to inqury at a plumbing company."},
                {"role": "user", "content": f"Classify this call transcript: {transcript}"}
            ],
            functions=functions,
            function_call={"name": "tag_call_category"}
        )
        tag= json.loads(response.choices[0].message.function_call.arguments)
        return tag['tag']
    
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return "Call back required"
