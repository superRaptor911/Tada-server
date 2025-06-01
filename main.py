from dotenv import load_dotenv
from gpt import gpt_simplify_text  # Import the function from gpt.py
from concurrent.futures import ThreadPoolExecutor
# Load environment variables from .env
load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configure CORS
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Allowed origins
    allow_credentials=True,            # Allow cookies and authentication
    allow_methods=["*"],               # Allow all HTTP methods
    allow_headers=["*"],               # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}



class Content(BaseModel):
    content: str

@app.post("/simplify")
def simplify_text(payload: Content):
    try:
        chunk_Size = 8000
        print(f"Received content of length: {len(payload.content)}")
        chunks = [payload.content[i:i + chunk_Size] for i in range(0, len(payload.content), chunk_Size)]
        responses = []
        with ThreadPoolExecutor() as executor:
            responses = list(executor.map(gpt_simplify_text, chunks))

        print(f"Processed {len(chunks)} chunks.")

        return {"content": "\n".join(responses)}
    except Exception as e:
        print(f"Error processing content: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",  # assume the file is named main.py
        host="0.0.0.0",  # listen on all available network interfaces
        port=8000,  # default port
        reload=True  # enable auto-reload for development
    )