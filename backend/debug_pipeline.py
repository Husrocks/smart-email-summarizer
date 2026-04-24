from transformers import pipeline
import transformers
print(f"Transformers version: {transformers.__version__}")
try:
    pipe = pipeline("summarization")
    print("Summarization pipeline created successfully")
except Exception as e:
    print(f"Error: {e}")

from transformers.pipelines import SUPPORTED_TASKS
print("Supported tasks:")
print(list(SUPPORTED_TASKS.keys()))
