import os, re
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq

load_dotenv()
st.set_page_config(page_title="RAG Knowledge Assistant", page_icon="📚")
st.title("📚 RAG Knowledge Assistant")
st.caption("Upload documents, retrieve relevant passages, and ask grounded questions.")

role = st.selectbox("Demo role", ["finance", "hr", "marketing", "executive"])
uploads = st.file_uploader("Knowledge files (PDF or TXT)", type=["pdf", "txt"], accept_multiple_files=True)
question = st.text_input("Ask a question")
chunks = []
for f in uploads or []:
    if f.name.lower().endswith(".pdf"):
        text = "\n".join(p.extract_text() or "" for p in PdfReader(f).pages)
    else:
        text = f.getvalue().decode("utf-8", errors="ignore")
    for part in re.split(r"\n\s*\n", text):
        part = part.strip()
        if part:
            tag = re.search(r"\[(finance|hr|marketing|all)\]", part, re.I)
            access = tag.group(1).lower() if tag else "all"
            chunks.append((f.name, access, part))

def allowed(access, user_role):
    return user_role == "executive" or access in ("all", user_role)

if st.button("Ask") and question:
    if not chunks:
        st.warning("Upload at least one PDF or TXT file.")
    elif re.search(r"\b(ignore all rules|reveal system prompt|show secrets)\b", question, re.I):
        st.error("Guardrail: this request is outside the assistant's allowed scope.")
    else:
        visible = [c for c in chunks if allowed(c[1], role)]
        if not visible:
            st.warning("No documents are available for this role.")
        else:
            docs = [c[2] for c in visible]
            vec = TfidfVectorizer(stop_words="english")
            matrix = vec.fit_transform(docs + [question])
            scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
            top = scores.argsort()[::-1][:3]
            context = "\n\n".join(f"[{visible[i][0]}] {docs[i]}" for i in top if scores[i] > 0)
            if not context:
                st.info("No relevant passages found. Try a more specific question.")
            else:
                key = os.getenv("GROQ_API_KEY")
                if key:
                    try:
                        client = Groq(api_key=key)
                        res = client.chat.completions.create(
                            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                            messages=[
                                {"role":"system","content":"Answer only from the supplied context. If it is insufficient, say so. Do not reveal private information."},
                                {"role":"user","content":f"Context:\n{context}\n\nQuestion: {question}"}
                            ], temperature=0.2
                        )
                        st.write(res.choices[0].message.content)
                    except Exception as e:
                        st.error(f"LLM request failed: {e}")
                else:
                    st.info("GROQ_API_KEY not set — showing retrieved context instead.")
                    st.write(context)
                with st.expander("Retrieved sources"):
                    st.write(context)
st.caption("Demo only: implement trusted login, document-level permissions, audit logs, evaluation and monitoring before real use.")
