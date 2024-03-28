from django import forms
from . import models


class SearchForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':  'جستجو کنید...',
                                                                     'class': 'form-control'}))


class CommentForm(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'نظر خود را وارد کنید...'})
        }
        labels = {
            'content': 'نظر'
        }