from django import forms

from premier_league.models import Guess

class ContactForm(forms.Form):
    name = forms.CharField(label='お名前')
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル')
    message = forms.CharField(label='メッセジー', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'お名前を入力してください'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスを入力してください'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルを入力してください'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセジーを入力してください'
        self.fields['message'].widget.attrs['class'] = 'form-control'

class GuessForm(forms.ModelForm):
    class Meta:
        model = Guess
        fields = ['team_1_score', 'team_2_score', 'guess_name']