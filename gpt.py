import openai
from typing import List, Dict, Any

MessageType = Dict[str, str] 

def get_ai_chat_response(messages: List[MessageType], model="gpt-4.1-mini-2025-04-14"):
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content  # Extract response text
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def gpt_simplify_text(text: str) -> str:
    messages = [
        {"role": "system", "content": "You will be given innerText of a webpage. " +
         "Your task is to simplify the text, making it easier to understand. "+
         "You should remove unwanted data that is not useful for the summary."},
        {"role": "user", "content": text}
    ]
    
    response = get_ai_chat_response(messages)
    print("got response from gpt")
    if response:
        return response
    else:
        return "Error in processing the request."