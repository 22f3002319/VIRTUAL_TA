# TDS Virtual TA - Deployment Guide

## Quick Deployment Options

### Option 1: Railway (Recommended - Free)
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect it's a Python app
6. Add environment variable: `OPENAI_API_KEY=your_key_here`
7. Deploy!

### Option 2: Render (Free)
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Set build command: `pip install -r requirements.txt && python setup.py`
6. Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
7. Add environment variable: `OPENAI_API_KEY=your_key_here`
8. Deploy!

### Option 3: Heroku (Paid)
1. Install Heroku CLI
2. Run: `heroku create your-app-name`
3. Run: `git push heroku main`
4. Set environment variable: `heroku config:set OPENAI_API_KEY=your_key_here`

### Option 4: Local with ngrok (For testing)
1. Install ngrok: `npm install -g ngrok`
2. Start your app: `uvicorn app:app --reload`
3. In another terminal: `ngrok http 8000`
4. Use the ngrok URL as your API endpoint

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for rubric evaluations

## Testing Your Deployment
```bash
# Test health endpoint
curl https://your-app-url.railway.app/health

# Test API endpoint
curl -X POST https://your-app-url.railway.app/api/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'
```

## Update YAML for Evaluation
After deployment, update `project-tds-virtual-ta-promptfoo.yaml`:
```yaml
providers:
  - id: https
    config:
      url: https://your-app-url.railway.app/api/  # Replace with your URL
```

Then run evaluation:
```bash
npx -y promptfoo eval --config project-tds-virtual-ta-promptfoo.yaml
``` 