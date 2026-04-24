import os
import pandas as pd
from transformers import AutoTokenizer
from datasets import Dataset, DatasetDict

MODEL_NAME = "google/flan-t5-base"

def tokenize_function(examples, tokenizer):
    # Prefix for T5
    inputs = ["summarize: " + doc for doc in examples["cleaned_text"]]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")

    # Fixed: Use text_target instead of as_target_tokenizer
    labels = tokenizer(text_target=examples["target_summary"], max_length=128, truncation=True, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def main():
    print(f"Loading tokenizer for {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    processed_dir = "data/processed"
    output_dir = "data/tokenized"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load processed CSVs into a DatasetDict
    data_files = {
        "train": os.path.join(processed_dir, "aeslc_train.csv"),
        "validation": os.path.join(processed_dir, "aeslc_validation.csv"),
        "test": os.path.join(processed_dir, "aeslc_test.csv")
    }
    
    # Check if files exist
    for split, path in data_files.items():
        if not os.path.exists(path):
            print(f"Warning: {path} not found. Run collect_data.py and preprocess.py first.")
            return

    raw_datasets = DatasetDict({
        split: Dataset.from_csv(path) for split, path in data_files.items()
    })

    print("Tokenizing datasets...")
    tokenized_datasets = raw_datasets.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True,
        remove_columns=raw_datasets["train"].column_names
    )

    print(f"Saving tokenized datasets to {output_dir}...")
    tokenized_datasets.save_to_disk(output_dir)
    print("Done!")

if __name__ == "__main__":
    main()
