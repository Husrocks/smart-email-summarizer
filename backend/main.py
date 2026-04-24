import logging
import gc
import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langdetect import detect, DetectorFactory

# Set seed for reproducible results from langdetect
DetectorFactory.seed = 0

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Smart Email Summarizer API")

# Enable CORS for Chrome Extension and Web Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeRequest(BaseModel):
    text: str
    length_setting: str = "medium"  # short, medium, long
    format: str = "paragraph"       # paragraph, bullets

class SummarizeResponse(BaseModel):
    summary: str
    language: str
    processing_time: float

# ── Model configuration ───────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEFT_PATH  = os.path.join(BASE_DIR, "models", "checkpoints", "email-summarizer-finetuned")
BASE_MODEL = "google/flan-t5-base"
FALLBACK   = "t5-small"

# Globals – loaded lazily on first request
_model     = None
_tokenizer = None

# ── Loader ────────────────────────────────────────────────────────────────────
def load_model():
    global _model, _tokenizer

    if _model is not None:
        return  # already loaded

    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    # Try to load fine-tuned PEFT model
    adapter_cfg = os.path.join(PEFT_PATH, "adapter_config.json")
    if os.path.exists(adapter_cfg):
        try:
            logger.info(f"Loading fine-tuned PEFT model from {PEFT_PATH} ...")
            from peft import PeftModel
            _tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
            base        = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL)
            _model      = PeftModel.from_pretrained(base, PEFT_PATH)
            _model.eval()
            logger.info("Fine-tuned model loaded successfully ✅")
            return
        except Exception as e:
            logger.error(f"Failed to load PEFT model: {e}")

    # Fallback – plain t5-small (no pipeline, same direct API)
    logger.info(f"Loading fallback model: {FALLBACK} ...")
    _tokenizer = AutoTokenizer.from_pretrained(FALLBACK)
    _model     = AutoModelForSeq2SeqLM.from_pretrained(FALLBACK)
    _model.eval()
    logger.info("Fallback model loaded ✅")


def unload_model():
    global _model, _tokenizer
    if _model is not None:
        logger.info("Unloading model to free memory...")
        _model     = None
        _tokenizer = None
        gc.collect()


# ── Summarize endpoint ────────────────────────────────────────────────────────
@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text is too short.")

    start_time = time.time()

    try:
        # Language detection
        try:
            lang = detect(request.text)
        except Exception:
            lang = "unknown"

        # Length constraints
        word_count = len(request.text.split())
        if request.length_setting == "short":
            max_len = max(20,  int(word_count * 0.20))
            min_len = max(10,  int(word_count * 0.10))
        elif request.length_setting == "long":
            max_len = max(150, int(word_count * 0.50))
            min_len = max(80,  int(word_count * 0.30))
        else:  # medium
            max_len = max(60,  int(word_count * 0.35))
            min_len = max(30,  int(word_count * 0.20))

        max_len = min(max_len, 512)
        min_len = min(min_len, max_len - 5)

        # Load model on first request
        load_model()

        # Truncate input to 800 words
        truncated = " ".join(request.text.split()[:800])
        prompt    = "summarize: " + truncated

        # Tokenize and generate
        import torch
        inputs  = _tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        with torch.no_grad():
            outputs = _model.generate(
                **inputs,
                max_new_tokens=max_len,
                min_new_tokens=min_len,
                do_sample=False,
                num_beams=4,
            )
        summary_text = _tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Format as bullets if requested
        if request.format == "bullets":
            sentences    = summary_text.replace(". ", ".\n").split("\n")
            summary_text = "\n".join(f"• {s.strip()}" for s in sentences if s.strip())

        processing_time = time.time() - start_time
        logger.info(f"Done in {processing_time:.2f}s | lang={lang}")

        return SummarizeResponse(
            summary=summary_text,
            language=lang,
            processing_time=processing_time,
        )

    except Exception as e:
        logger.error(f"Summarization error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {e}")


@app.get("/health")
async def health():
    peft_loaded = _model is not None and hasattr(_model, 'peft_config')
    return {
        "status": "healthy",
        "model": "fine-tuned PEFT (flan-t5-base)" if peft_loaded else FALLBACK,
        "peft_model_loaded": peft_loaded,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
