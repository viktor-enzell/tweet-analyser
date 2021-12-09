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
    comment_sentiment = sentiment_model.fit_predict(comments)
    tweet_has_comments = len(comments) > 0
    if tweet_has_comments:
        sentiment_model.get_boxplot()

    return {
        'request_success': len(tweet) > 0,
        'tweet': tweet,
        'tweet_has_comments': tweet_has_comments,
        'comment_sentiment': comment_sentiment * 100,
    }


def multi_tweet_data(username):
    return {
        'request_success': True,
    }
