from django import forms


class TweetIDForm(forms.Form):
    tweet_id_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Enter a link to a Tweet or a Tweet ID...'
        })
    )
