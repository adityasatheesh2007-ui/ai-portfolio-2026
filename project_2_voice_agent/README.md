# 2. Voice Support Assistant
Run: `streamlit run project_2_voice_agent/app.py`

Upload a short audio recording (WAV/MP3/M4A), transcribe it using Groq Whisper, generate a support
reply with Groq, then create spoken output using gTTS. Requires `GROQ_API_KEY`; internet access is
needed for API calls and gTTS. This is a web-demo workflow, not a telephony integration.
