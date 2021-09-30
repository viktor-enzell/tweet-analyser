from django.shortcuts import render
from .forms import TextForm
from random import randrange


def make_prediction(text):
    return 0 == randrange(2)


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
                    context = {
                        'text_form': text_form,
                        'text': text,
                        'sentiment_is_positive': make_prediction(text)
                    }
                    return render(request, 'index.html', context)

        text_form = TextForm()
        context = {
            'text_form': text_form,
        }
        return render(request, 'index.html', context)
