from flask import Flask, render_template, request
import pandas as pd
from textblob import TextBlob

app = Flask(__name__)

# Load music dataset
music_df = pd.read_csv('music.csv')

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return 'Happy'
    elif polarity < -0.1:
        return 'Sad'
    else:
        return 'Neutral'

def recommend_music(sentiment, n):
    # Filter by genre based on sentiment and sort by rating in descending order
    if sentiment == 'Happy':
        filtered_df = music_df[music_df['genre'].isin(['Pop', 'Dance'])].sort_values(by='rating', ascending=False)
    elif sentiment == 'Sad':
        filtered_df = music_df[music_df['genre'].isin(['Blues', 'Acoustic'])].sort_values(by='rating', ascending=False)
    else:
        filtered_df = music_df[music_df['genre'].isin(['Rock', 'Classical'])].sort_values(by='rating', ascending=False)
    
    # Return up to n recommendations, or all available if n exceeds the number of songs
    return filtered_df.head(n).to_dict('records')

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = None
    sentiment = None
    num_recommendations = 3  # Default value
    if request.method == 'POST':
        user_text = request.form['user_text']
        num_recommendations = int(request.form.get('num_recommendations', 3))  # Get user-specified number, default to 3
        sentiment = analyze_sentiment(user_text)
        recommendations = recommend_music(sentiment, num_recommendations)
    return render_template('index.html', recommendations=recommendations, sentiment=sentiment, num_recommendations=num_recommendations)

if __name__ == '__main__':
    app.run(debug=True)