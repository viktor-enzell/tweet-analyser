from django.shortcuts import render
from .forms import TextForm
from .sentiment_model import SentimentModel
from .twitter_client import TwitterClient

twitter_client = TwitterClient()
sentiment_model = SentimentModel()


def index(request):
    """
    Handling all GET and POST requests.
    """
    if request.method == 'GET':
        if request.GET.get('text', False):
            text_form = TextForm(request.GET)
            if text_form.is_valid():
                text = text_form.cleaned_data.get('text', False)
                if text:
                    request.session['text'] = text
                    comments = twitter_client.get_comments(text)
                    sentiment = sentiment_model.fit_predict(comments)
                    context = {
                        'text_form': text_form,
                        'text': text,
                        'sentiment_is_positive': sentiment > 0.5
                    }
                    return render(request, 'index.html', context)

        text_form = TextForm()
        context = {
            'text_form': text_form,
        }
        return render(request, 'index.html', context)
