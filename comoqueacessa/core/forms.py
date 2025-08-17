from django import forms

class Form_de_busca(forms.Form):
    query = forms.CharField(label="Qual a sua dúvida?", max_length=300)