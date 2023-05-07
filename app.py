from flask import Flask, render_template
import requests
from dateutil.parser import parse
from dateutil import tz


def format_date(date_str):
    date_obj = parse(date_str)
    local_timezone = tz.tzlocal()
    date_obj = date_obj.astimezone(local_timezone)
    return date_obj.strftime("%B %d, %Y %I:%M %p")

app = Flask(__name__)

@app.route('/')
def index():
    # Define the keywords you want to search for
    keywords = ['cybersecurity', 'cyber', 'zero-day vulnerability', 'Azure', 'AWS', 'zero day', 'zero-trust', 'cloud security', 'kubernetes', 'kubernetes security']

    # Replace 'your_api_key' with your actual Bing Search API key
    api_key = 'da52ae7de2dc41f8a2033b7f2f8868a0'

    # Make API calls to Bing Search API to fetch articles
    articles = []
    seen_urls = set()  # Keep track of article URLs to avoid duplicates
    headers = {'Ocp-Apim-Subscription-Key': api_key}
    for keyword in keywords:
        url = f'https://api.bing.microsoft.com/v7.0/news/search?q={keyword}&count=10&sortBy=Date'
        response = requests.get(url, headers=headers)
        data = response.json()

        if 'value' in data:
            for article in data['value']:
                if article['url'] not in seen_urls:
                    article['formattedDate'] = format_date(article['datePublished'])
                    articles.append(article)
                    seen_urls.add(article['url'])

    # Sort the articles by their published time in descending order
    articles.sort(key=lambda x: x['datePublished'], reverse=True)

    # Limit the number of articles to display
    articles = articles[:10]

    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
