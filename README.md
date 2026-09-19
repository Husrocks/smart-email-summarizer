<div align="center">
  <h1>📧 SmartSummarize — End-to-End LLM Email Project</h1>
  
  <p>
    <strong>A high-performance AI platform that transforms long emails into concise, actionable summaries.</strong>
  </p>
  
  <p>
    <a href="https://github.com/Husrocks/smart-email-summarizer/stargazers"><img src="https://img.shields.io/github/stars/Husrocks/smart-email-summarizer?style=for-the-badge&color=yellow" alt="Stars"/></a>
    <a href="https://github.com/Husrocks/smart-email-summarizer/network/members"><img src="https://img.shields.io/github/forks/Husrocks/smart-email-summarizer?style=for-the-badge&color=orange" alt="Forks"/></a>
    <a href="https://github.com/Husrocks/smart-email-summarizer/issues"><img src="https://img.shields.io/github/issues/Husrocks/smart-email-summarizer?style=for-the-badge&color=red" alt="Issues"/></a>
    <a href="https://github.com/Husrocks/smart-email-summarizer/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Husrocks/smart-email-summarizer?style=for-the-badge&color=blue" alt="License"/></a>
  </p>
</div>

---

## 📖 About the Project

**SmartSummarize** is a complete, end-to-end Machine Learning ecosystem designed to solve the problem of email overload. Unlike standard generic tools, this project leverages a custom **fine-tuned Flan-T5-Base** model, trained specifically on over 18,000 real-world emails from the AESLC dataset. 

It provides seamless integration into your daily workflow through a **Chrome Extension**, an elegant **Web Dashboard**, and a robust **FastAPI Backend**.

## ✨ Key Features

- 🧠 **Fine-tuned LLM:** Custom weights trained on the AESLC email dataset using LoRA for highly accurate summarization.
- 📩 **Gmail Integration:** Automatically reads and summarizes open emails directly within your Gmail interface.
- 🎨 **Web Dashboard:** A premium, dark-themed dashboard for direct text summarization.
- 🧩 **Chrome Extension:** Quick-access tool featuring a right-click "Summarize This" context menu support.
- ⚙️ **Dual Mode:** Choose between succinct *Paragraph* or structured *Bullet Point* summaries.
- ⚡ **Fast Inference:** Optimized to run efficiently on local CPUs—no expensive GPU required for inference.

## 🛠️ Architecture & Tech Stack

- **Model:** `google/flan-t5-base` fine-tuned via LoRA (Low-Rank Adaptation)
- **Backend:** Python, FastAPI, Hugging Face Transformers, PyTorch
- **Frontend:** HTML5, Vanilla CSS (Premium Dark Theme), JavaScript
- **Extension:** Chrome Extension API (Manifest V3)
- **Dataset:** AESLC (Annotated Enron Subject Line Corpus) - 18,000 samples

## 🚀 Getting Started

Follow these instructions to set up the project locally on your machine.

### 1. Prerequisites
- Python 3.9+
- Google Chrome Browser
- Git

### 2. Backend Setup (The AI Engine)
1. Clone this repository:
   ```bash
   git clone https://github.com/Husrocks/smart-email-summarizer.git
   cd smart-email-summarizer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Start the backend FastAPI server:
   ```bash
   python backend/main.py
   ```
   > **Note:** On the first run, the system will download the base Flan-T5 model (~900MB) and load your custom fine-tuned weights automatically.

### 3. Web Dashboard Setup
1. Navigate to the `frontend/` directory.
2. Open `index.html` in any modern web browser.
3. Ensure your backend server is running, paste your text, and start summarizing!

### 4. Chrome Extension Setup

#### Option A: Pre-packaged (Easiest)
1. Download [`smart-email-summarizer-extension.zip`](./smart-email-summarizer-extension.zip) from the repository root.
2. Extract the ZIP file to a known location.
3. Open Chrome and navigate to `chrome://extensions/`.
4. Enable **Developer mode** (top right corner).
5. Click **Load unpacked** and select the extracted folder.

#### Option B: From Source
1. Open Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode**.
3. Click **Load unpacked** and select the `extension/` folder from this project directory.
4. **Important:** Click the extension icon in your toolbar once to ensure it connects to the running backend.

## 💡 Usage Guide

- **In Gmail:** Open any email, click the SmartSummarize extension icon in your toolbar, and it will automatically extract and summarize the email body.
- **Right-Click Feature:** Highlight text on *any* webpage, right-click, and select **"Summarize This"**. The extension popup will display the generated summary.
- **Web App:** Use the standalone web application for custom text inputs and length adjustments (Short, Medium, Long).

## 📁 Project Structure

```text
smart-email-summarizer/
├── backend/       # FastAPI server and model inference logic
├── extension/     # Chrome Extension (MV3) with Gmail auto-detection
├── frontend/      # Premium web dashboard (HTML/CSS/JS)
├── training/      # Training scripts used to fine-tune the model
├── scripts/       # Data collection and preprocessing pipeline
├── models/        # Fine-tuned LoRA weights and checkpoints
└── README.md      # Project documentation
```

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the terms specified in the [LICENSE](./LICENSE) file. See `LICENSE` for more information.

---
<div align="center">
  <p>Developed with ❤️ for Advanced AI Research.</p>
</div>
