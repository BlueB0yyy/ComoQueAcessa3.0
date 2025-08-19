from django import forms

class Form_de_busca(forms.Form):
    query = forms.CharField(label="Como acessar", max_length=300)