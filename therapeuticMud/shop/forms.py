from django import forms


class Review_form(forms.Form):
    
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'class':'form-control'}))