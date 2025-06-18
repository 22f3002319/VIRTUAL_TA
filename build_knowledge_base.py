import json
import os
from datetime import datetime

def build_knowledge_base():
    """Build unified knowledge base from course content and discourse posts"""
    
    knowledge_base = {
        "course_content": [],
        "discourse_posts": [],
        "metadata": {
            "created_date": datetime.now().isoformat(),
            "total_items": 0,
            "course_content_count": 0,
            "discourse_posts_count": 0
        }
    }
    
    # Load course content
    course_content_path = os.path.join("data", "course_content.json")
    if os.path.exists(course_content_path):
        with open(course_content_path, "r", encoding="utf-8") as f:
            course_content = json.load(f)
            knowledge_base["course_content"] = course_content
            knowledge_base["metadata"]["course_content_count"] = len(course_content)
            print(f"Loaded {len(course_content)} course content items")
    
    # Load discourse posts
    discourse_path = os.path.join("data", "discourse.json")
    if os.path.exists(discourse_path):
        with open(discourse_path, "r", encoding="utf-8") as f:
            discourse_posts = json.load(f)
            knowledge_base["discourse_posts"] = discourse_posts
            knowledge_base["metadata"]["discourse_posts_count"] = len(discourse_posts)
            print(f"Loaded {len(discourse_posts)} discourse posts")
    
    # Update total count
    knowledge_base["metadata"]["total_items"] = (
        knowledge_base["metadata"]["course_content_count"] + 
        knowledge_base["metadata"]["discourse_posts_count"]
    )
    
    # Save unified knowledge base
    output_path = os.path.join("data", "knowledge_base.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    print(f"Built knowledge base with {knowledge_base['metadata']['total_items']} total items")
    print(f"Saved to: {output_path}")
    
    return knowledge_base

if __name__ == "__main__":
    build_knowledge_base() 