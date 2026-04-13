# 📄 Document Summarization Refinement
A local AI-powered PDF summarization app built with Streamlit and Ollama. Upload a PDF, generate an iteratively refined summary, extract key points, and download everything — all running privately on your machine with no API keys or internet required.

---

## Features
- **Iterative Refinement** — generates an initial summary, then refines it over multiple passes to improve clarity, completeness, and accuracy
- **Side-by-side Comparison** — view the initial and final summary together to see how refinement improved the output
- **Key Points Extraction** — automatically pulls the 5 most important points from the document as a numbered list
- **Model Selector** — switch between locally installed Ollama models from the sidebar without editing code
- **Download Outputs** — download the initial summary, final summary, and key points as `.txt` files named after your original document
- **Persistent Results** — results stay on screen after downloading; no data is lost between button clicks
- **Fully Local** — runs entirely on your machine using Ollama; no data is sent to any external server

---

## Tools & Technologies Used

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web UI framework for the app interface |
| [Ollama](https://ollama.com) | Local LLM runtime — runs AI models on your machine |
| [LangChain](https://www.langchain.com) | Prompt templating and LLM orchestration |
| [PyPDF2](https://pypdf2.readthedocs.io) | PDF text extraction |
| [Python 3.10+](https://www.python.org) | Core programming language |

### Models Supported
| Model | Provider |
|-------|---------|
| `deepseek-r1:1.5b` | DeepSeek |
| `phi3:mini` | Microsoft |
| `llama3.2:1b` | Meta |
| `llama3.1` | Meta |

---

## Requirements
- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- At least one Ollama model pulled (see below)

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/document-summarizer.git
cd document-summarizer
```

**2. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**3. Install and start Ollama**

Download from [https://ollama.com](https://ollama.com), then pull a model:
```bash
ollama pull deepseek-r1:1.5b
```

Other supported models (add more in the sidebar selectbox):
```bash
ollama pull phi3:mini
ollama pull llama3.2:1b
```

**4. Run the app**
```bash
python -m streamlit run app-auto-refinement-summarizer.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage
1. Upload a PDF file using the file uploader
2. Select the number of refinement iterations using the slider (more iterations = more refined summary, but takes longer)
3. Choose your preferred AI model from the sidebar
4. Click **Generate Summary**
5. View the initial summary, refined final summary, and key points
6. Download any or all outputs as `.txt` files

---

## Model Recommendations

| Model | Size | Quality | Works On |
|-------|------|---------|----------|
| `deepseek-r1:1.5b` | 1.1 GB | Good | Low RAM (4GB+) |
| `phi3:mini` | 2.3 GB | Very Good | Medium RAM (6GB+) |
| `llama3.2:1b` | 700 MB | Decent | Low RAM (3GB+) |
| `llama3.1` | 4.9 GB | Excellent | High RAM (8GB+) |

If your machine has less than 8GB RAM, stick with `deepseek-r1:1.5b` or `llama3.2:1b`.

---

## Project Structure

```
document-summarizer/
│
├── app-auto-refinement-summarizer.py       # Main Streamlit app
├── main_auto-refinment_summarizer.ipynb    # Helper notebook (for development)
├── README.md                               # This file
└── requirements.txt                        # Python dependencies
```

---

## Known Limitations
- Large PDFs are truncated to the first ~4000 characters to prevent memory crashes on low-RAM machines
- `llama3.1` (8B) may crash with a 500 error on machines with less than 8GB RAM — use a smaller model in that case
- First run may be slow as Ollama loads the model into memory

---

## License
MIT License — feel free to use, modify, and distribute.