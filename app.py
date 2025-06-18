from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

class LinkResponse(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[LinkResponse]

# Load knowledge base from file
def load_knowledge_base():
    """Load knowledge base from JSON file"""
    try:
        with open("data/knowledge_base.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: knowledge_base.json not found, using fallback data")
        return {
            "course_content": [],
            "discourse_posts": []
        }

KNOWLEDGE_BASE = load_knowledge_base()

def search_knowledge_base(question: str, image: Optional[str] = None) -> List[dict]:
    """Enhanced search function with better matching"""
    results = []
    question_lower = question.lower()
    
    # Search in course content
    for item in KNOWLEDGE_BASE.get("course_content", []):
        score = 0
        # Check title
        if item.get("title") and any(keyword in item["title"].lower() for keyword in question_lower.split()):
            score += 2
        # Check content
        if item.get("content") and any(keyword in item["content"].lower() for keyword in question_lower.split()):
            score += 1
        # Check tags
        if item.get("tags") and any(keyword in question_lower for keyword in item["tags"]):
            score += 3
        
        if score > 0:
            item["score"] = score
            results.append(item)
    
    # Search in discourse posts
    for item in KNOWLEDGE_BASE.get("discourse_posts", []):
        score = 0
        # Check title
        if item.get("title") and any(keyword in item["title"].lower() for keyword in question_lower.split()):
            score += 2
        # Check content
        if item.get("content") and any(keyword in item["content"].lower() for keyword in question_lower.split()):
            score += 1
        
        if score > 0:
            item["score"] = score
            results.append(item)
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return results

@app.post("/api/", response_model=AnswerResponse)
async def answer_question(req: QuestionRequest):
    """Answer student questions"""
    try:
        # Search for relevant content
        relevant_items = search_knowledge_base(req.question, req.image)
        
        if not relevant_items:
            return AnswerResponse(
                answer="I am sorry, I could not find a specific answer to your question in the course materials or discussion forums. Please check the course documentation or ask your question in the Discourse forum.",
                links=[]
            )
        
        # Use the best matching item
        top_result = relevant_items[0]
        answer = top_result["content"]
        
        # Generate links
        links = []
        for item in relevant_items[:3]:
            link_text = item.get("title", "Relevant content")
            links.append(LinkResponse(url=item["url"], text=link_text))
        
        return AnswerResponse(answer=answer, links=links)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "knowledge_base_loaded": True,
        "total_items": len(KNOWLEDGE_BASE.get("course_content", [])) + len(KNOWLEDGE_BASE.get("discourse_posts", []))
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "TDS Virtual TA API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "api": "/api/",
            "docs": "/docs"
        },
        "usage": {
            "method": "POST",
            "url": "/api/",
            "body": {
                "question": "Your question here",
                "image": "base64_encoded_image_optional"
            }
        }
    }
