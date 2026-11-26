# 5. Hybrid Log Classifier
Run: `streamlit run project_5_hybrid_log_classifier/app.py`

The pipeline uses exact-pattern regex rules first, a Logistic Regression model trained on a tiny
illustrative sample second, and optional Groq fallback for ambiguous messages. Replace the sample
training examples with a properly labeled dataset and evaluate on held-out data before use.
