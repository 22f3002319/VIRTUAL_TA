import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def scrape_discourse(category_url, start_date, end_date, output_path):
    posts = []
    page = 0
    while True:
        page_url = f"{category_url}?page={page}"
        resp = requests.get(page_url)
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        topics = soup.select(".topic-list-item")
        if not topics:
            break
        for topic in topics:
            link = topic.find("a", class_="title")
            if not link:
                continue
            url = link['href']
            title = link.text.strip()
            date_str = topic.find("span", class_="relative-date")
            if date_str:
                # Try to parse date, fallback if not possible
                try:
                    post_date = datetime.strptime(date_str['title'][:10], "%Y-%m-%d")
                except Exception:
                    continue
                if not (start_date <= post_date <= end_date):
                    continue
            # Fetch post contentV  
            post_resp = requests.get(url)
            if post_resp.status_code != 200:
                continue
            post_soup = BeautifulSoup(post_resp.text, "html.parser")
            content_div = post_soup.find("div", class_="post")
            content = content_div.text.strip() if content_div else ""
            posts.append({"url": url, "title": title, "content": content})
        page += 1
    if posts:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
    else:
        print("No posts found. discourse.json not overwritten.")

if __name__ == "__main__":
    # Example usage
    category_url = "https://discourse.onlinedegree.iitm.ac.in/c/tds"
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 4, 14)
    output_path = os.path.join("data", "discourse.json")
    scrape_discourse(category_url, start_date, end_date, output_path)
