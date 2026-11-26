# 1. RAG Knowledge Assistant
Run: `streamlit run project_1_rag/app.py`

Upload TXT/PDF knowledge files, select a demo role, and ask questions. The MVP uses TF-IDF
retrieval and a simple role-tag convention (`[finance]`, `[hr]`, `[marketing]`, `[all]`) before
sending retrieved excerpts to Groq. Without a key, it displays retrieved context.

**Important:** Role selection is a teaching simulation, not real authentication. Production RBAC
must derive roles from a trusted identity provider and enforce access on the server.
