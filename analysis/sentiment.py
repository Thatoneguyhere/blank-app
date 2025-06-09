from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def get_sentiment_score(headlines):
    sentiments = sentiment_pipeline(headlines)
    scores = [1 if s["label"] == "POSITIVE" else -1 if s["label"] == "NEGATIVE" else 0 for s in sentiments]
    avg_score = sum(scores) / len(scores)
    return avg_score
