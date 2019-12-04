from django import forms

class CuponApplyForm(forms.Form):
    code = forms.CharField()
