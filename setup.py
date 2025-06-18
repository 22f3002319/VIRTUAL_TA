#!/usr/bin/env python3
"""
Setup script for TDS Virtual TA
This script will:
1. Scrape course content
2. Scrape discourse posts
3. Build the unified knowledge base
4. Install dependencies
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Setting up TDS Virtual TA...")
    
    # Step 1: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Step 2: Create data directory
    os.makedirs("data", exist_ok=True)
    print("✅ Created data directory")
    
    # Step 3: Scrape course content
    if not run_command("python scrape_course_content.py", "Scraping course content"):
        print("Warning: Course content scraping failed, but continuing...")
    
    # Step 4: Scrape discourse posts
    if not run_command("python scrape_discourse.py", "Scraping discourse posts"):
        print("Warning: Discourse scraping failed, but continuing...")
    
    # Step 5: Build knowledge base
    if not run_command("python build_knowledge_base.py", "Building knowledge base"):
        print("Warning: Knowledge base building failed, but continuing...")
    
    print("\n🎉 Setup completed!")
    print("\nTo start the API server, run:")
    print("uvicorn app:app --reload")
    print("\nThe API will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 