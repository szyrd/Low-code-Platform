#!/usr/bin/env python3
"""
Debug script to test page saving API
"""
import requests
import json

# API configuration
BASE_URL = "http://localhost:8000/api"
USERNAME = "yerdana"  # Replace with actual username
PASSWORD = "admin"  # Replace with actual password

def login():
    """Login and get access token"""
    url = f"{BASE_URL}/auth/token/"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        tokens = response.json()
        print("Login successful")
        return tokens['access']
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return None

def test_save_page(access_token):
    """Test saving a page"""
    url = f"{BASE_URL}/pages/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Test page data
    page_data = {
        "name": "Test Page",
        "project": 16,  # Adjust project ID as needed
        "layout_config": {
            "components": [
                {
                    "id": "test-component-1",
                    "type": "Button",
                    "x": 0,
                    "y": 0,
                    "w": 4,
                    "h": 2,
                    "props": {
                        "label": "Test Button",
                        "color": "primary"
                    }
                }
            ]
        }
    }
    
    print("Sending request to save page...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(page_data, indent=2)}")
    
    response = requests.post(url, json=page_data, headers=headers)
    
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Response content: {response.text}")
    
    if response.status_code == 201:
        print("Page saved successfully!")
        return response.json()
    else:
        print("Failed to save page")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print("Could not parse error response as JSON")
        return None

def main():
    print("Testing page save API...")
    
    # Login
    access_token = login()
    if not access_token:
        print("Cannot proceed without access token")
        return
    
    # Test save page
    result = test_save_page(access_token)
    if result:
        print(f"Success! Created page with ID: {result.get('id')}")
    else:
        print("Page save test failed")

if __name__ == "__main__":
    main() 