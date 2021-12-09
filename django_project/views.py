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
    """
    {
    "tweet_sentiment": ,
    "average_comment_sentiment": ,
    "max_reply": {
        "text" : ,
        "sentiment" : 
    },
    "min_reply": {
        "text" : ,
        "sentiment" : 
    },
    """
    # if tweet_has_comments:
    #     sentiment_model.get_boxplot()
    print('hello', type(tweet_data))
    comment_sentiment = tweet_data['average_comment_sentiment']

    if comment_sentiment < 0.5:
        comment_sentiment_color = f'rgb(255,0,0,{1 - comment_sentiment})'  # Red
    else:
        comment_sentiment_color = f'rgb(61,255,0,{comment_sentiment})'  # Green

    return {
        'request_success': len(tweet['text']) > 0,
        'tweet': tweet,
        'tweet_has_comments': len(comments) > 0,
        'tweet_sentiment': tweet_data['tweet_sentiment'],
        'comment_sentiment': comment_sentiment,
        'comment_sentiment_percent': round(comment_sentiment * 100, 1),
        'comment_sentiment_color': comment_sentiment_color,
    }


def multi_tweet_data(username):
    tweets = twitter_client.get_user_tweets(username)
    ind_analysed_tweets = []
    for tweet in tweets:
        print('tweet', tweet)
        ind_analysed_tweets.append(single_tweet_data(tweet['id']))

    name = ind_analysed_tweets[0]['tweet']['name'] if len(ind_analysed_tweets) > 0 else ''

    return {
        'request_success': len(tweets) > 0,
        'tweets': ind_analysed_tweets,
        'name': name,
        'num_tweets': len(ind_analysed_tweets)
    }
