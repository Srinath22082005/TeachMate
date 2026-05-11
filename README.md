
# 📘 TeachMate AI Agent

**TeachMate AI Agent** is a Streamlit-powered, Gemini-integrated application that empowers educators with AI tools for productivity, lesson planning, syllabus generation, assessments, resource recommendations, feedback analysis, and RAG-powered Q&A.

---

## ✅ Features

- 📘 **Syllabus Generator** – Auto-generate weekly academic plans
- 🧾 **Lesson Plan Creator** – Topic, activities, and outcome-based breakdowns
- 📝 **Assessment Builder** – MCQs, short/long answer and Bloom’s taxonomy
- 🔍 **Resource Recommender** – Suggests videos, blogs, PDFs, papers
- 📊 **Feedback Tracker** – Weekly review and AI improvement suggestions
- 🤖 **AI Co-Pilot** – Ask anything about teaching or planning
- 📂 **RAG Document Uploader** – Upload PDFs, DOCX, TXT
- 💡 **RAG-Powered Q&A** – Ask questions based on your own documents

---

## 📁 Folder Structure

```
teachmate_ai_agent/
├── app/
│   ├── ui/                  # Streamlit UI tabs
│   ├── agents/              # Gemini-based logic agents
│   ├── rag/                 # ChromaDB vector search
│   ├── utils/               # File exporter, watermark, role utils
│   ├── memory/              # Stores .docx, .json logs
├── docs/sample_pdfs/        # Upload your course materials here
├── requirements.txt
├── .env.template
├── streamlit_app.py
└── README.md
```

---

## 🛠️ Installation

### 1. Clone and Set Up
```bash
git clone https://github.com/yourname/teachmate_ai_agent.git
cd teachmate_ai_agent
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
# OR
source venv/bin/activate     # macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Gemini API Key

- Copy `.env.template` to `.env`
- Paste your API key from: https://aistudio.google.com/app/apikey

```
GOOGLE_API_KEY=your_api_key_here
```

---

## 🚀 Run the App

Make sure you run from **project root** (not inside /app):

```bash
# Windows
$env:PYTHONPATH="C:\teachmate_ai_agent"
 streamlit run C:\teachmate_ai_agent\app\streamlit_app.py


# macOS/Linux
export PYTHONPATH=.
streamlit run app/streamlit_app.py
```

---

## 🧠 Gemini SDK Integration

We use the official `google-generativeai` SDK:

```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
```

---

## 🧪 Supported File Types for RAG

Upload PDFs, DOCX, or TXT files via **RAG Document Uploader**. Then use **RAG Q&A** to ask questions based on content.

---

## 🛠 Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'app'` | Run from project root + set `PYTHONPATH=.` |
| `TypeError: GenerativeModel got unexpected keyword 'api_key'` | Use `genai.configure()` instead of passing `api_key` directly |
| `streamlit_app.py` not found | Run `streamlit run app/streamlit_app.py` from root |

---

