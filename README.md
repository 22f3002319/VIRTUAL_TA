# TDS Virtual TA

A virtual Teaching Assistant Discourse responder for IIT Madras' Online Degree in Data Science.

## Features
- REST API to answer student questions using course content and Discourse posts
- **NEW**: Support for base64 image attachments in questions
- **NEW**: Enhanced search algorithm with semantic matching
- **NEW**: Course content scraping from TDS course website
- **NEW**: Unified knowledge base combining course materials and forum posts
- **NEW**: Improved error handling and response validation

## Quick Setup
1. Clone the repo and run the setup script:
   ```bash
   python setup.py
   ```
   This will automatically:
   - Install dependencies
   - Scrape course content
   - Scrape Discourse posts
   - Build the unified knowledge base

2. Start the API:
   ```bash
   uvicorn app:app --reload
   ```

## Manual Setup (Alternative)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Scrape data:
   ```bash
   python scrape_course_content.py
   python scrape_discourse.py
   python build_knowledge_base.py
   ```

3. Run the API:
   ```bash
   uvicorn app:app --reload
   ```

## API Usage

### Basic Question
```bash
curl "http://localhost:8000/api/" \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I use gpt-4o-mini or gpt-3.5-turbo?"}'
```

### Question with Image
```bash
curl "http://localhost:8000/api/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does this screenshot show?",
    "image": "base64_encoded_image_data"
  }'
```

### Response Format
```json
{
  "answer": "You must use gpt-3.5-turbo-0125, even if the AI Proxy only supports gpt-4o-mini...",
  "links": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939",
      "text": "Use the model that's mentioned in the question."
    }
  ]
}
```

## Knowledge Base

The system uses a unified knowledge base containing:

### Course Content
- Docker and Containerization guidelines
- OpenAI API usage instructions
- GA4 and GA5 assignment guidelines
- Course setup and grading information

### Discourse Posts
- Student questions and answers from Jan 1, 2025 - Apr 14, 2025
- Clarifications and discussions
- Common troubleshooting topics

## Search Algorithm

The improved search algorithm includes:
- **Exact phrase matching** (highest priority)
- **Word overlap scoring** for content and titles
- **Keyword matching** for TDS-specific terms
- **Image text integration** (when provided)
- **Semantic relevance scoring**

## API Endpoints

- `POST /api/` - Answer questions (main endpoint)
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

## Deployment

### Quick Deploy Options

**Railway (Recommended - Free):**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Add environment variable: `OPENAI_API_KEY=your_key_here`
6. Deploy!

**Render (Free):**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect this repository
5. Set build command: `pip install -r requirements.txt && python setup.py`
6. Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
7. Add environment variable: `OPENAI_API_KEY=your_key_here`
8. Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Testing
Run the evaluation tests:
```bash
npx -y promptfoo eval --config project-tds-virtual-ta-promptfoo.yaml
```

## Submission

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy your application** (see Deployment section above)

3. **Update YAML file** with your deployed URL:
   ```yaml
   providers:
     - id: https
       config:
         url: https://your-app-url.railway.app/api/
   ```

4. **Submit at:** https://exam.sanand.workers.dev/tds-project-virtual-ta
   - GitHub repository URL
   - API endpoint URL

## License
MIT 
