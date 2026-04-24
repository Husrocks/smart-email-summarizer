# Smart Email Summarizer

An AI-powered tool that converts long emails into concise summaries using Hugging Face Transformers. Includes a Python FastAPI backend and a Chrome Extension.

## Features

- **Abstractive Summarization**: Uses the `distilbart-cnn-12-6` model for high-quality, fast summaries.
- **Adjustable Length**: Choose between Short, Medium, and Long summaries.
- **Multiple Formats**: Output as structured bullet points or cohesive paragraphs.
- **Language Detection**: Automatically detects the input language.
- **Chrome Extension**: Right-click context menu and popup interface for quick access.
- **Copy to Clipboard**: One-click copying of summaries.

## 🛠 Setup Instructions

### 1. Backend Setup

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```
2.  **Create a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the server**:
    ```bash
    python main.py
    ```
    The backend will run at `http://127.0.0.1:8000`. The first request will trigger the model download (~400MB).

### 2. Extension Installation

1.  Open Chrome and navigate to `chrome://extensions/`.
2.  Enable **Developer mode** (toggle in the top right).
3.  Click **Load unpacked**.
4.  Select the `extension` folder from this project directory.

## 🚀 Usage

1.  **Direct Paste**: Click the extension icon in your toolbar, paste the email text, and click "Generate Summary".
2.  **Context Menu**: Highlight any text on a webpage, right-click, and select **"Summarize This"**. The extension popup will open with the text pre-filled.
3.  **Customization**: Use the slider to adjust length and the toggle buttons to switch between paragraph and bullet formats.

## 📁 Project Structure

- `backend/`: FastAPI application and AI logic.
- `extension/`: Chrome Extension manifest, UI, and background scripts.
- `create_placeholders.py`: Utility script to generate extension icons.

## 📝 Technical Notes

- **Model**: `sshleifer/distilbart-cnn-12-6` (Optimized for speed/quality).
- **Backend**: FastAPI with CORS enabled for extension communication.
- **Memory**: The model is loaded on-demand. Subsequent requests are faster as the model stays in memory for the session duration.
