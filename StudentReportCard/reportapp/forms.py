from django import forms

class EmailForm(forms.ModelForm):
    email = forms.EmailField()