# 5 AI Projects That Will Matter in 2026

A collection of five educational Streamlit MVPs based on the supplied
`5 AI Projects That Will Matter in 2026` PDF.

## Projects
1. **RAG Knowledge Assistant** — document retrieval, role-based access demo, basic guardrails.
2. **Voice Support Assistant** — speech-to-text upload, LLM response, text-to-speech output.
3. **Multi-Agent Coding Assistant** — planner → architect → coder workflow; downloads generated files as ZIP.
4. **Multimodal Document Assistant** — asks questions about uploaded images and PDFs.
5. **Hybrid Log Classifier** — regex rules → Logistic Regression → optional LLM fallback.

These are educational MVPs, not production deployments. The RBAC demo is not a substitute for
server-side identity and authorization. Do not upload confidential documents or real personal data.

## Quick start
- Python 3.10+
- Copy `.env.example` to `.env` and add a Groq API key (optional for deterministic/demo features;
  required for LLM-powered answers).
- Install dependencies: `pip install -r requirements.txt`
- Run one project: `streamlit run project_1_rag/app.py`
- Replace the path with any other `project_*` app.

Get a Groq API key at https://console.groq.com/keys. Never commit `.env` or API keys.

## GitHub
Clone this repository, then run:

```bash
git clone https://github.com/adityasatheesh2007-ui/ai-portfolio-2026.git
cd ai-portfolio-2026
pip install -r requirements.txt
streamlit run project_1_rag/app.py
```

## Project-specific notes
Each project folder has its own README. Some capabilities require API keys
and/or optional packages. Check each README before running.
