import re
from textblob import TextBlob

def clean_text(text):
  text = re.sub(r'@[A-Za-z0-9:]+', '', text)
  text = re.sub(r'#', '', text)
  text = re.sub(r'RT[\s]', '', text)
  text = re.sub(r'https?:\/\/\S+', '', text)
  return text

def get_subjectivity(text):
  return TextBlob(text).sentiment.subjectivity

def get_polarity(text):
  return TextBlob(text).sentiment.polarity

def get_sentiment(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'
