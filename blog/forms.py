from django import forms
from django.forms import widgets
from .models import *

class EditorForm(forms.Form):
    title = forms.CharField(max_length=100, widget=widgets.Textarea(attrs={
        'class': "ipt BNE_txtA",
    }))
    body = forms.CharField(widget=widgets.Textarea(attrs={
        'class': "tar BNE_txtA",
    }))
    category = forms.ChoiceField(label='分类', choices=Category.objects.values_list())
