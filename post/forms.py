from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':  'جستجو کنید...',
                                                                     'class': 'form-control'}))