import requests
import json

def test_summarization():
    url = "http://127.0.0.1:8000/summarize"
    payload = {
        "text": """
        Subject: Project Update - Q3 Strategy

        Hi Team,

        I hope you're all doing well. I wanted to provide a quick update on our Q3 strategy. 
        We have decided to pivot our focus slightly towards mobile-first development given the recent user trends we've observed. 
        The marketing team will be launching the new campaign on August 15th. 
        Please ensure all design assets are ready by the end of next week. 
        We also need to schedule a follow-up meeting to discuss the budget allocations for the upcoming quarter.
        
        Best regards,
        Sarah
        """,
        "length_setting": "medium",
        "format": "bullets"
    }
    
    try:
        print("Sending request to backend...")
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Summary received:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Failed to connect to backend: {e}")

if __name__ == "__main__":
    test_summarization()
