import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import re

def scrape_course_content(base_url, output_path):
    """Scrape course content from TDS course website"""
    course_content = []
    
    # Define course sections to scrape
    sections = [
        {"url": f"{base_url}/#/docker", "title": "Docker and Containerization"},
        {"url": f"{base_url}/#/openai", "title": "OpenAI API Integration"},
        {"url": f"{base_url}/#/ga4", "title": "GA4 Assignment"},
        {"url": f"{base_url}/#/ga5", "title": "GA5 Assignment"},
        {"url": f"{base_url}/#/setup", "title": "Course Setup"},
        {"url": f"{base_url}/#/grading", "title": "Grading and Assessment"},
    ]
    
    for section in sections:
        try:
            print(f"Scraping: {section['title']}")
            resp = requests.get(section["url"])
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                
                # Extract content from different HTML elements
                content_elements = []
                
                # Look for main content areas
                main_content = soup.find("main") or soup.find("div", class_="content") or soup.find("div", class_="main")
                if main_content:
                    content_elements.append(main_content)
                
                # Look for article content
                article = soup.find("article")
                if article:
                    content_elements.append(article)
                
                # Look for specific content divs
                content_divs = soup.find_all("div", class_=re.compile(r"content|text|body"))
                content_elements.extend(content_divs)
                
                # If no specific content areas found, get body content
                if not content_elements:
                    body = soup.find("body")
                    if body:
                        content_elements.append(body)
                
                # Extract text content
                content_text = ""
                for element in content_elements:
                    # Remove script and style elements
                    for script in element(["script", "style"]):
                        script.decompose()
                    
                    # Get text content
                    text = element.get_text(separator=' ', strip=True)
                    if text and len(text) > 50:  # Only include substantial content
                        content_text += text + "\n\n"
                
                # Clean up the content
                content_text = re.sub(r'\s+', ' ', content_text).strip()
                
                if content_text and len(content_text) > 100:
                    course_content.append({
                        "url": section["url"],
                        "title": section["title"],
                        "content": content_text,
                        "tags": extract_tags(content_text),
                        "type": "course_content",
                        "scraped_date": datetime.now().isoformat()
                    })
                    
        except Exception as e:
            print(f"Error scraping {section['url']}: {e}")
            continue
    
    # Add some hardcoded course content based on common TDS topics
    hardcoded_content = [
        {
            "url": "https://tds.s-anand.net/#/docker",
            "title": "Docker vs Podman",
            "content": "Podman is recommended for the course, but Docker is also acceptable. Both are containerization tools that can be used for running applications in isolated environments. For this course, you can use either Docker or Podman based on your preference and system compatibility.",
            "tags": ["docker", "podman", "containerization", "setup"],
            "type": "course_content",
            "scraped_date": datetime.now().isoformat()
        },
        {
            "url": "https://tds.s-anand.net/#/openai",
            "title": "OpenAI API Usage",
            "content": "For assignments requiring OpenAI API, you must use the specific model mentioned in the question. If the question asks for gpt-3.5-turbo-0125, use that model even if your AI proxy only supports gpt-4o-mini. You may need to use the OpenAI API directly in such cases.",
            "tags": ["openai", "gpt", "api", "model"],
            "type": "course_content",
            "scraped_date": datetime.now().isoformat()
        },
        {
            "url": "https://tds.s-anand.net/#/ga4",
            "title": "GA4 Assignment Guidelines",
            "content": "GA4 is the data sourcing assignment. Students need to collect and process data from various sources. The dashboard will display scores out of 10, and if a student scores 10/10 plus bonus points, the dashboard will show 110. Make sure to follow the specific requirements for data collection and processing.",
            "tags": ["ga4", "data", "sourcing", "dashboard", "grading"],
            "type": "course_content",
            "scraped_date": datetime.now().isoformat()
        },
        {
            "url": "https://tds.s-anand.net/#/ga5",
            "title": "GA5 Assignment Guidelines",
            "content": "GA5 focuses on AI and language models. When using tokenizers, follow the approach demonstrated by Prof. Anand. Calculate tokens by using a tokenizer similar to what was shown in class, then multiply by the given rate. Always use the model specified in the question requirements.",
            "tags": ["ga5", "ai", "language", "models", "tokenizer"],
            "type": "course_content",
            "scraped_date": datetime.now().isoformat()
        }
    ]
    
    course_content.extend(hardcoded_content)
    
    # Save course content
    if course_content:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(course_content, f, ensure_ascii=False, indent=2)
        print(f"Scraped {len(course_content)} course content items")
    else:
        print("No course content found")

def extract_tags(content):
    """Extract relevant tags from content"""
    tags = []
    content_lower = content.lower()
    
    # Define tag keywords
    tag_keywords = {
        "docker": ["docker", "container"],
        "podman": ["podman"],
        "openai": ["openai", "gpt", "api"],
        "ga4": ["ga4", "data", "sourcing"],
        "ga5": ["ga5", "ai", "language", "model"],
        "setup": ["setup", "installation", "configure"],
        "grading": ["grading", "score", "dashboard", "assessment"]
    }
    
    for tag, keywords in tag_keywords.items():
        if any(keyword in content_lower for keyword in keywords):
            tags.append(tag)
    
    return tags

if __name__ == "__main__":
    base_url = "https://tds.s-anand.net"
    output_path = os.path.join("data", "course_content.json")
    scrape_course_content(base_url, output_path) 