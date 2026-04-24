import os
from datasets import load_dataset
import pandas as pd

def collect_aeslc():
    print("Downloading AESLC dataset from Hugging Face...")
    dataset = load_dataset("aeslc")
    
    # Save to CSV for easy inspection/preprocessing
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    for split in dataset.keys():
        df = pd.DataFrame(dataset[split])
        output_path = os.path.join(output_dir, f"aeslc_{split}.csv")
        df.to_csv(output_path, index=False)
        print(f"Saved {split} split to {output_path}")

if __name__ == "__main__":
    collect_aeslc()
