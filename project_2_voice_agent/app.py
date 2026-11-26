import os, tempfile
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS

load_dotenv()
st.set_page_config(page_title="Voice Support Agent", page_icon="🎙️")
st.title("🎙️ Voice Support Agent")
st.write("Upload a customer voice message → transcribe → respond → listen.")
audio = st.file_uploader("Audio file", type=["wav", "mp3", "m4a", "mpeg"])
key = os.getenv("GROQ_API_KEY")
if audio and st.button("Process voice message"):
    if not key:
        st.error("Add GROQ_API_KEY to your .env file first.")
    else:
        try:
            client = Groq(api_key=key)
            suffix = "." + audio.name.split(".")[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(audio.getvalue()); path = tmp.name
            with open(path, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    file=(audio.name, f.read()), model="whisper-large-v3", response_format="text"
                )
            os.unlink(path)
            st.subheader("Transcript")
            st.write(transcript)
            answer = client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                messages=[
                    {"role":"system","content":"You are a concise, polite customer support assistant. Never invent order or account details. Ask for missing information."},
                    {"role":"user","content":str(transcript)}
                ], temperature=0.3
            ).choices[0].message.content
            st.subheader("Assistant response")
            st.write(answer)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as out:
                outpath = out.name
            gTTS(answer).save(outpath)
            st.audio(outpath, format="audio/mp3")
            with open(outpath, "rb") as f:
                st.download_button("Download spoken reply", f, "support_reply.mp3", "audio/mpeg")
            os.unlink(outpath)
        except Exception as e:
            st.error(f"Could not process audio: {e}")
