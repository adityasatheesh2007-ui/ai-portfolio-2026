import os, re
import streamlit as st
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from groq import Groq

load_dotenv()
st.set_page_config(page_title="Hybrid Log Classifier", page_icon="🧪")
st.title("🧪 Hybrid Log Classifier")
st.caption("Regex → Statistical ML → optional LLM fallback")

TRAIN_X = [
 "authentication failed for user", "multiple failed login attempts", "suspicious login detected",
 "out of memory process killed", "disk space is almost full", "cpu usage exceeded threshold",
 "database connection refused", "sql query timeout", "database server unavailable",
 "deployment failed", "job execution error", "task workflow could not complete",
 "backup completed successfully", "user logged in", "service started successfully"
]
TRAIN_Y = [
 "Security Alert","Security Alert","Security Alert",
 "Resource Usage","Resource Usage","Resource Usage",
 "Database Error","Database Error","Database Error",
 "Workflow Error","Workflow Error","Workflow Error",
 "Info","Info","Info"
]
model = Pipeline([("tfidf",TfidfVectorizer(ngram_range=(1,2))),( "clf",LogisticRegression(max_iter=1000))])
model.fit(TRAIN_X,TRAIN_Y)

def classify(text):
    patterns = [
        (r"(failed login|authentication failed|suspicious login|security breach)", "Security Alert"),
        (r"(out of memory|disk space|cpu usage|memory usage)", "Resource Usage"),
        (r"(database.*(refused|unavailable|timeout)|sql.*timeout)", "Database Error"),
        (r"(deployment failed|workflow.*(failed|error)|task.*could not complete)", "Workflow Error")
    ]
    for pattern, label in patterns:
        if re.search(pattern,text,re.I):
            return label, "Regex", 1.0
    probs = model.predict_proba([text])[0]
    idx = probs.argmax()
    confidence = float(probs[idx])
    if confidence >= 0.48:
        return model.classes_[idx], "Logistic Regression", confidence
    return "Unknown", "LLM fallback", confidence

logs = st.text_area("Paste a programming/system log", "Multiple failed login attempts detected for user 9052")
if st.button("Classify") and logs.strip():
    label, method, confidence = classify(logs)
    if label == "Unknown" and os.getenv("GROQ_API_KEY"):
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            answer = client.chat.completions.create(
                model=os.getenv("GROQ_MODEL","llama-3.3-70b-versatile"),
                messages=[
                    {"role":"system","content":"Classify this log into exactly one category: Security Alert, Resource Usage, Database Error, Workflow Error, Info. Return only the category. If uncertain return Unknown."},
                    {"role":"user","content":logs}
                ], temperature=0
            ).choices[0].message.content.strip()
            allowed = ["Security Alert","Resource Usage","Database Error","Workflow Error","Info","Unknown"]
            label = next((x for x in allowed if x.lower() in answer.lower()),"Unknown")
        except Exception as e:
            st.warning(f"LLM fallback unavailable: {e}")
    st.metric("Predicted category", label)
    st.write(f"Method: **{method}** · ML confidence: **{confidence:.1%}**")
    st.info("Illustrative training data only. Confidence is not a calibrated probability.")
