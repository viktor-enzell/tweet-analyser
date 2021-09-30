from django import forms


class TextForm(forms.Form):
    text = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Enter some text...'
        })
    )
