import openai
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()

client = OpenAI()


MessageType = Dict[str, str] 

def get_ai_chat_response(messages: List[MessageType], model="gpt-4.1-mini-2025-04-14"):
    try:
        response = client.responses.create(
            model=model,
            input=messages,
            stream=True,
        )

        
        full_response = ""
        for event in response:
            delta = getattr(event, "delta", "") # getattr(object, name[, default])
            print(delta, end="", flush=True)  # Print live to stdout
            full_response += delta

        print()  # Final newline after response
        return response.output_text

    
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
    
async def get_simplify_text_stream(text: str):
    messages = [
        {"role": "system", "content": "You will be given innerText of a webpage. Your task is to simplify the text, making it easier to understand. You should not change the meaning of the text, but rather make it more accessible."},
        {"role": "user", "content": text}
    ]
    
    try:
        stream = client.responses.create(
            model="gpt-4.1-mini-2025-04-14",
            input=messages,
            stream=True
        )

        for event in stream:
            delta = getattr(event, "delta", "")
            print(delta, end="", flush=True)
            yield delta  # Yield each part of the response as it comes in
            await asyncio.sleep(0) # Simulate async behavior
    except Exception as e:
        print(f"Error: {e}")
        yield "Error in processing the request."