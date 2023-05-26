from django import forms


class ReviewForm(forms.Form):
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'class':'form-control'}))


class OrderForm(forms.Form):
    address = forms.CharField(label='Адрес доставки', widget=forms.Textarea(attrs={'class': 'form-control'}))
    payment_method = forms.ChoiceField(label='Способ оплаты', choices=[(0, "Наличный расчет"), (1, "Безналичный расчет")], widget=forms.Select(attrs={'class': 'form-select'}))

