import os
import json
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI(title="Catchy Headline Generator")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class TopicRequest(BaseModel):
    topic: str

class HeadlineResponse(BaseModel):
    headlines: List[str]

# --- Static File Serving ---
@app.get("/")
async def serve_index():
    return FileResponse('index.html')

@app.get("/style.css")
async def serve_css():
    return FileResponse('style.css')

@app.get("/script.js")
async def serve_js():
    return FileResponse('script.js')

# --- API Endpoints ---
@app.post("/generate", response_model=HeadlineResponse)
async def generate_headlines(request: TopicRequest):
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required")
    
    prompt = f"""
    Generate 10 "click-worthy", catchy, and viral headlines for a YouTube video or Blog posts about the topic: "{request.topic}".
    The headlines should be engaging, use power words, and pique curiosity.
    Return ONLY a JSON array of strings, nothing else.
    Example: ["10 Exercises You Can Do at Home", "Shocking Truth About Exercise"]
    """
    
    try:
        if not api_key:
            raise ValueError("No API Key configured")
            
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up Markdown formatting
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        headlines = json.loads(text)
        if not isinstance(headlines, list):
            raise ValueError("LLM did not return a list")
            
        return HeadlineResponse(headlines=headlines)
    
    except Exception as e:
        logger.error(f"Error generating headlines: {e}")
        # Fallback Headlines
        fallback = [
            f"10 {request.topic} Secrets You Never Knew",
            f"Why Your {request.topic} Routine Is Failing (And How to Fix It)",
            f"The Ultimate Guide to Mastering {request.topic} in 2025",
            f"Is {request.topic} the Key to a Better Life? What Science Says",
            f"Shocking Truth About {request.topic}: Don't Be Fooled",
            f"How I Improved My {request.topic} With This One Simple Trick",
            f"Expert Reveals the Best Way to Approach {request.topic}",
            f"7 Common Mistakes Everyone Makes with {request.topic}",
            f"Transform Your Life with These {request.topic} Hacks",
            f"The Future of {request.topic}: What to Expect Next"
        ]
        return HeadlineResponse(headlines=fallback)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
