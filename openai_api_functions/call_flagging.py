import openai
import json 
# from secret_key import openai_key
# openai.api_key= openai_key
openai_key="insertyourkeyhere"
openai.api_key= openai_key

functions = [
    {
        "name": "flag_call_category",
        "description": "Flag the call transcript into a category.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["Verbal loop", "Incomplete call", "Hallucinate", "Reading prompt", "None"],
                    "description": "The category that best describes the flagging of the call.",
                },
            },
            "required": ["category"],
        },
    }
]


def flag_call_via_openai(transcript: str) -> str:
    """
    Calls the OpenAI API to flag the call transcript using function calling.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  
            messages=[
                {"role": "system", "content": "You are an assistant who flags call transcripts."},
                {"role": "user", "content": f"Flag this call transcript: {transcript}"}
            ],
            functions=functions,
            function_call={"name": "flag_call_category"}
        )

        flag_category= json.loads(response.choices[0].message.function_call.arguments)
        return flag_category['category']
        

    except Exception as e:
        print("heleleo")
        print(f"Error in OpenAI API call: {e}")
        return "None"
