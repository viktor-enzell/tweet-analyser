from django.shortcuts import render
from .forms import TweetIDForm
from .sentiment_model import SentimentModel
from .twitter_client import TwitterClient

twitter_client = TwitterClient()
sentiment_model = SentimentModel()


def index(request):
    """
    Handling all GET and POST requests.
    """
    if request.method == 'GET':
        if request.GET.get('tweet_id_input', False):
            tweet_id_form = TweetIDForm(request.GET)
            if tweet_id_form.is_valid():
                tweet_id_input = tweet_id_form.cleaned_data.get('tweet_id_input', False)
                if tweet_id_input:
                    request.session['tweet_id_input'] = tweet_id_input
                    parsed_input = twitter_client.parse_id_or_username(tweet_id_input)
                    single_tweet = parsed_input.isnumeric()

                    context = {
                        'request_made': True,
                        'tweet_id_form': tweet_id_form,
                        'tweet_id_input': tweet_id_input,
                        'single_tweet': single_tweet,
                    }
                    if single_tweet:
                        context.update(single_tweet_data(parsed_input))
                    else:
                        context.update(multi_tweet_data(parsed_input))

                    return render(request, 'index.html', context)

        tweet_id_form = TweetIDForm()
        context = {
            'tweet_id_form': tweet_id_form,
        }
        return render(request, 'index.html', context)


def single_tweet_data(tweet_id):
    tweet = twitter_client.get_tweet(tweet_id)
    comments = twitter_client.get_comments(tweet_id)

    tweet_data = sentiment_model.fit_predict(comments, tweet["text"])

    tweet_data.update(tweet)
    tweet_data['comments'] = comments
    tweet_data['tweet_has_comments'] = len(comments) > 0

    # Sentiment as percent
    tweet_data['tweet_sentiment_percent'] = round(tweet_data['tweet_sentiment'] * 100, 1)
    tweet_data['average_comment_sentiment_percent'] = round(tweet_data['average_comment_sentiment'] * 100, 1)
    tweet_data['max_reply']['sentiment_percent'] = round(tweet_data['max_reply']['sentiment'] * 100, 1)
    tweet_data['min_reply']['sentiment_percent'] = round(tweet_data['min_reply']['sentiment'] * 100, 1)

    # Add colors
    tweet_data['tweet_sentiment_color'] = get_color(tweet_data['tweet_sentiment'])
    tweet_data['comment_sentiment_color'] = get_color(tweet_data['average_comment_sentiment'])
    tweet_data['max_reply']['color'] = get_color(tweet_data['max_reply']['sentiment'])
    tweet_data['min_reply']['color'] = get_color(tweet_data['min_reply']['sentiment'])

    return {
        'request_success': len(tweet['text']) > 0,
        'tweet_data': tweet_data,
    }


def multi_tweet_data(username):
    tweets = twitter_client.get_user_tweets(username)
    analysed_tweets = []
    for tweet in tweets:
        analysed_tweets.append(single_tweet_data(tweet['id']))

    # TODO: Replace dummy below with:
    #  multi_tweet_sentiment = twitter_client.get_multi_tweet_sentiment(tweets)
    tweets_data = {
        'average': 0.5,
        'best': 3,
        'worst': 5,
    }
    best = analysed_tweets[tweets_data['best']]['tweet_data']
    worst = analysed_tweets[tweets_data['worst']]['tweet_data']

    # Best and worst tweet texts
    tweets_data['best_text'] = best['text']
    tweets_data['worst_text'] = worst['text']

    # Sentiment as percent
    tweets_data['average_percent'] = round(tweets_data['average'] * 100, 1)
    tweets_data['best_average_comment_percent'] = best['average_comment_sentiment_percent']
    tweets_data['worst_average_comment_percent'] = worst['average_comment_sentiment_percent']

    # Add colors
    tweets_data['average_color'] = get_color(tweets_data['average'])
    tweets_data['best_color'] = best['comment_sentiment_color']
    tweets_data['worst_color'] = worst['comment_sentiment_color']

    return {
        'request_success': len(tweets) > 0,
        'tweets': analysed_tweets,
        'tweets_data': tweets_data,
        'name': analysed_tweets[0]['tweet_data']['name'] if len(analysed_tweets) > 0 else '',
        'num_tweets': len(analysed_tweets),
    }


def get_color(sentiment):
    if sentiment < 0.5:
        # Red
        return f'rgb(255,0,0,{1 - sentiment})'
    else:
        # Green
        return f'rgb(61,255,0,{sentiment})'
