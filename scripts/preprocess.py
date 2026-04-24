import os
import pandas as pd
import re
from bs4 import BeautifulSoup

def clean_email_body(text):
    # Remove HTML tags if any
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # Remove common email headers (Subject is usually separate in AESLC)
    text = re.sub(r'From:.*?\n', '', text)
    text = re.sub(r'To:.*?\n', '', text)
    text = re.sub(r'Cc:.*?\n', '', text)
    text = re.sub(r'Sent:.*?\n', '', text)
    
    # Remove multiple whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_data():
    input_dir = "data/raw"
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(input_dir) if f.startswith("aeslc_") and f.endswith(".csv")]
    
    for file in files:
        print(f"Preprocessing {file}...")
        df = pd.read_csv(os.path.join(input_dir, file))
        
        # In AESLC: 'email_body' is the source, 'subject_line' is the target summary
        df['cleaned_text'] = df['email_body'].apply(clean_email_body)
        df['target_summary'] = df['subject_line'].astype(str).str.strip()
        
        # Remove empty or very short entries
        df = df[df['cleaned_text'].str.len() > 20]
        df = df[df['target_summary'].str.len() > 5]
        
        output_path = os.path.join(output_dir, file.replace("raw", "processed"))
        df[['cleaned_text', 'target_summary']].to_csv(output_path, index=False)
        print(f"Saved preprocessed data to {output_path}")

if __name__ == "__main__":
    preprocess_data()
