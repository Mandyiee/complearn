from django import forms
from purpose.models import Purpose

class PurposeForm(forms.ModelForm):
    class Meta:
        model = Purpose
        fields = '__all__'
        widgets = {
            'usage': forms.TextInput(attrs={'class': 'form-control'}),
            'tensile_strength': forms.TextInput(attrs={'class': 'form-control'}),
            'young_modulus': forms.TextInput(attrs={'class': 'form-control'}),
        }