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

                    tweet_id = twitter_client.parse_tweet_id(tweet_id_input)

                    tweet = twitter_client.get_tweet(tweet_id)
                    comments = twitter_client.get_comments(tweet_id)
                    tweet_retrieved = len(tweet) > 0 and len(comments) > 0

                    sentiment = sentiment_model.fit_predict(comments)
                    sentiment_model.get_boxplot()

                    context = {
                        'tweet_id_form': tweet_id_form,
                        'tweet_id_input': tweet_id_input,
                        'tweet_retrieved': tweet_retrieved,
                        'tweet': tweet,
                        'sentiment_is_positive': sentiment > 0.5,
                        'sentiment': sentiment * 100,
                    }
                    return render(request, 'index.html', context)

        tweet_id_form = TweetIDForm()
        context = {
            'tweet_id_form': tweet_id_form,
        }
        return render(request, 'index.html', context)
