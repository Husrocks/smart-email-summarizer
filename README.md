# 🎓 SmartSummarize — End-to-End LLM Email Project

**SmartSummarize** is a high-performance AI platform that transforms long emails into concise summaries. Unlike standard tools, this project uses a custom **fine-tuned Flan-T5-Base** model trained specifically on 18,000+ real-world emails.

---

## 🚀 Key Features

- **Fine-tuned LLM**: Custom weights trained on the AESLC email dataset using LoRA.
- **Gmail Integration**: Automatically reads and summarizes open emails in Gmail.
- **Web Dashboard**: A premium, dark-themed dashboard for direct use.
- **Chrome Extension**: Quick-access tool with right-click "Summarize This" support.
- **Dual Mode**: Choose between Paragraph or Bullet Point summaries.
- **Fast Inference**: Optimized to run on local CPUs (no GPU needed for use).

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.9 or higher
- Google Chrome Browser

### 2. Backend Setup (The AI Engine)
1. Clone this repository and navigate to the project root.
2. Install the required libraries:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Start the backend server:
   ```bash
   python backend/main.py
   ```
   *Note: The first time you run this, it will download the base Flan-T5 model (~900MB). It will then load your custom fine-tuned weights.*

### 3. Chrome Extension Setup

**Option A: Pre-packaged (easiest)**
1. [Download `smart-email-summarizer-extension.zip`](./smart-email-summarizer-extension.zip) from this repository.
2. Extract the ZIP file to a folder.
3. Open Chrome and go to `chrome://extensions/`.
4. Turn on **Developer mode** (top right).
5. Click **Load unpacked** and select the extracted folder.

**Option B: From Source**
1. Open Chrome and go to `chrome://extensions/`.
2. Turn on **Developer mode** (top right).
3. Click **Load unpacked**.
4. Select the `extension` folder from this project directory.
5. **Important:** Click the extension icon in your toolbar to ensure it's connected to the backend.

### 4. Web Dashboard Setup
1. Navigate to the `frontend` folder.
2. Open `index.html` in any web browser.
3. Make sure your backend is running, then start summarizing!

---

## 📖 How to Use

### 📧 Using in Gmail
1. Open any email in your Gmail tab.
2. Click the **SmartSummarize** extension icon in your Chrome toolbar.
3. The extension will automatically grab the email text and generate a summary!

### 🖱️ Right-Click Feature
1. Highlight any text on any webpage.
2. Right-click and select **"Summarize This"**.
3. The extension popup will open with your summary ready.

### 💻 Using the Web App
1. Open `frontend/index.html`.
2. Paste any text into the box, choose your length (Short/Medium/Long), and hit **Generate**.

---

## 🧠 Model Technical Details
- **Base Model**: `google/flan-t5-base`
- **Training Technique**: LoRA (Low-Rank Adaptation)
- **Parameters Trained**: 1.7 Million (0.7% of total)
- **Dataset**: AESLC (Annotated Enron Subject Line Corpus) - 18,000 samples.
- **Inference**: CPU-optimized direct generation.

---

## 📁 Project Structure
- `backend/`: FastAPI server and inference logic.
- `extension/`: Chrome Extension (MV3) with Gmail auto-detection.
- `frontend/`: Premium web dashboard.
- `training/`: Training scripts used to fine-tune the model.
- `scripts/`: Data collection and preprocessing pipeline.
- `models/`: Fine-tuned LoRA weights and checkpoints.

---

## 🤝 Contributing
Feel free to fork this project and submit pull requests for any features or bug fixes.

---

**Developed with ❤️ for Advanced AI Research.**
