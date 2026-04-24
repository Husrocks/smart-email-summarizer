import os
from datasets import load_from_disk
from transformers import (
    AutoModelForSeq2SeqLM, 
    AutoTokenizer, 
    DataCollatorForSeq2Seq, 
    Seq2SeqTrainingArguments, 
    Seq2SeqTrainer
)
from peft import LoraConfig, get_peft_model, TaskType
import torch

MODEL_NAME = "google/flan-t5-base"
DATA_PATH = "data/tokenized"
OUTPUT_DIR = "models/checkpoints/email-summarizer-finetuned"

def train():
    # 1. Load Data
    print(f"Loading tokenized data from {DATA_PATH}...")
    tokenized_datasets = load_from_disk(DATA_PATH)
    
    # 2. Load Base Model
    print(f"Loading base model {MODEL_NAME}...")
    device_map = "auto" if torch.cuda.is_available() else None
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, device_map=device_map)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # 3. Apply LoRA (Parameter Efficient Fine-Tuning)
    print("Applying LoRA configuration...")
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q", "v"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.SEQ_2_SEQ_LM
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # 4. Define Training Arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        predict_with_generate=True,
        fp16=torch.cuda.is_available(), # Use FP16 if GPU is available
        learning_rate=5e-4,
        num_train_epochs=3,
        logging_steps=100,
        eval_strategy="epoch", # Fixed: Renamed from evaluation_strategy
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=True,
        report_to="none", # Change to "wandb" if using WandB
        push_to_hub=False,
    )

    # 5. Data Collator
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    # 6. Initialize Trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        data_collator=data_collator,
    )

    # 7. Start Training
    print("Starting training...")
    trainer.train()

    # 8. Save final model
    print(f"Saving final model to {OUTPUT_DIR}...")
    trainer.save_model(OUTPUT_DIR)
    print("Training Complete!")

if __name__ == "__main__":
    train()
