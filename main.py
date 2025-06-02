from dotenv import load_dotenv
from gpt import gpt_simplify_text  # Import the function from gpt.py
from concurrent.futures import ThreadPoolExecutor
from gpt import get_simplify_text_stream


# Load environment variables from .env
load_dotenv()


from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

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
    
@app.websocket("/ws/simplify")
async def websocket_simplify(websocket: WebSocket):
    await websocket.accept() #connection accepted
    print("WebSocket connection established.")
    print("Waiting for data...")
    try:
        while True:
            data = await websocket.receive_text()
            if not data:
                print("No data received, closing connection.")
                await websocket.close()
                return
            print("Data received, processing...")
            # Process the received data
            print(f"Received data: {data}")

            chunk_size = 8000
            chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
            
            for chunk in chunks:
                print(f"Processing chunk of size {len(chunk)}")

                async for tokens in get_simplify_text_stream(chunk):
                    # print(f"Sending token: {tokens}")
                    await websocket.send_text(tokens)
            print("All chunks processed")
            
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",  # assume the file is named main.py
        host="0.0.0.0",  # listen on all available network interfaces
        port=8000,  # default port
        reload=True  # enable auto-reload for development
    )