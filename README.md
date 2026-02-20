# Catchy Headline Generator

Generate click-worthy titles for your YouTube videos and Blogs using AI.

## Features

- **AI-Powered**: Uses Gemini LLM to generate 10 catchy headlines.
- **Glassmorphism UI**: Beautiful, modern design with smooth animations.
- **Copy to Clipboard**: Quick copy functionality for results.
- **Fast & Responsive**: Works instantly on desktop and mobile.

## Technology Stack

- **Backend**: FastAPI (Python)
- **AI**: Google Gemini (generative-ai)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+)

## Setup & Running

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure AI (Optional)**:
   Create a `.env` file and add your Google API key:
   ```env
   GOOGLE_API_KEY=your_actual_key_here
   ```
   *If no key is provided, the app will use a fallback mock generator for demonstration.*

3. **Run the Backend**:
   ```bash
   python main.py
   ```

4. **Launch Frontend**:
   Open `index.html` in your favorite web browser.

## Project Structure

```
headline-generator/
├── main.py             # FastAPI Backend
├── index.html          # Frontend UI
├── style.css           # Premium Styling
├── script.js           # Frontend Logic
├── requirements.txt    # Dependencies
└── .env                # Environment Variables (Optional)
```
