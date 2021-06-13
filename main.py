import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "P7FEEGDXXECOBSTM"
NEWS_API_KEY = "1c5a322ed48b46e39bae5f45f649dffb"

TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_VIRTUAL_NUMBER = "+"
TWILIO_DESTINATION_NUMBER = "+"

stock_params = {"function": "TIME_SERIES_DAILY", "symbol": STOCK_NAME, "apikey": STOCK_API_KEY}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
diff_percent = (difference / float(yesterday_closing_price)) * 100

# In order to check if this is working we must set the value to a number lower than the percentage.
# The required value for the exercise is 5
if diff_percent > 0:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    first_three_articles = articles[:3]

    formatted_news = [
        f"Headline: {article['title']}.\nBrief: {article['description']}" for article in first_three_articles
    ]

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_news:
        message = client.messages.create(
            body=article,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_DESTINATION_NUMBER,
        )
