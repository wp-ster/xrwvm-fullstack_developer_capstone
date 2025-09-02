import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Direct URL assignment to avoid environment variable issues
backend_url = "https: //rickon221450-3030.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http: //localhost: 5050/")

print(f"🔗 Backend URL set to: {backend_url}")

def get_request(endpoint, **kwargs):
    # Construct the full URL
    request_url = backend_url + endpoint

    # Add parameters if provided
    if kwargs:
        params = "&".join([f"{key}={value}" for key, value in kwargs.items()])
        request_url += "?" + params

    print(f"🚀 Making GET request to: {request_url}")

    try:
        response = requests.get(request_url, timeout=30)
        print(f"📊 Response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Received {len(data) if isinstance(data, list) else 1} items from backend")
            return data
        else:
            print(f"❌ Bad response: {response.status_code} - {response.text}")
            return []

    except requests.exceptions.Timeout:
        print(f"⏰ Timeout calling {request_url}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"🌐 Request failed for {request_url}: {e}")
        return []
    except Exception as e:
        print(f"💥 Unexpected error for {request_url}: {e}")
        return []

def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Post review failed: {e}")
        return None

def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        response = requests.get(request_url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Sentiment analysis failed: {e}")
        return {"sentiment": "neutral"}


