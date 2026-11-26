import os, base64
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from groq import Groq

load_dotenv()
st.set_page_config(page_title="Multimodal Assistant", page_icon="🧾")
st.title("🧾 Multimodal Document Assistant")
file = st.file_uploader("Upload an image or PDF", type=["png","jpg","jpeg","webp","pdf"])
question = st.text_input("What would you like to know?", "Summarize this document and identify the important amounts.")
if st.button("Analyze"):
    if not file:
        st.warning("Upload an image or PDF.")
    elif not os.getenv("GROQ_API_KEY"):
        st.error("Add GROQ_API_KEY to .env first.")
    else:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        try:
            if file.name.lower().endswith(".pdf"):
                text = "\n".join(p.extract_text() or "" for p in PdfReader(file).pages)
                if not text.strip():
                    st.error("No selectable text found in this PDF. Try an image or OCR-enabled PDF.")
                else:
                    result = client.chat.completions.create(
                        model=os.getenv("GROQ_MODEL","llama-3.3-70b-versatile"),
                        messages=[
                            {"role":"system","content":"Analyze only the supplied document text. Distinguish visible facts from assumptions. Never claim a charge is fraudulent without evidence."},
                            {"role":"user","content":f"Document text:\n{text[:18000]}\n\nQuestion: {question}"}
                        ], temperature=0.2
                    )
                    st.write(result.choices[0].message.content)
            else:
                mime = file.type or "image/jpeg"
                encoded = base64.b64encode(file.getvalue()).decode()
                result = client.chat.completions.create(
                    model=os.getenv("GROQ_VISION_MODEL","llama-3.2-11b-vision-preview"),
                    messages=[{"role":"user","content":[
                        {"type":"text","text":f"Carefully inspect this document image. Answer using only visible evidence; state uncertainty. Question: {question}"},
                        {"type":"image_url","image_url":{"url":f"data:{mime};base64,{encoded}"}}
                    ]}], temperature=0.2
                )
                st.write(result.choices[0].message.content)
        except Exception as e:
            st.error(f"Analysis failed. Check model availability and API limits: {e}")
