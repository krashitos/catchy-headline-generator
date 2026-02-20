import os
import json
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
if not api_key:
    # Attempt to get from environment or fallback to a placeholder if it's handled by Antigravity's system
    # In this environment, the agent usually has access to the tool for LLM calls or the key is injected.
    # However, since I'm building a standalone webapp, I'll expect it in .env or system env.
    logger.warning("GOOGLE_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI(title="Catchy Headline Generator API")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopicRequest(BaseModel):
    topic: str

class HeadlineResponse(BaseModel):
    headlines: List[str]

@app.get("/")
async def root():
    return {"message": "Catchy Headline Generator API is running"}

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
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up Markdown formatting if present
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
        # Mock fallback for demonstration
        fallback_headlines = [
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
        return HeadlineResponse(headlines=fallback_headlines)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
