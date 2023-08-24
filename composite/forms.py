from django import forms
from .models import Composite

class CompositeForm(forms.Form):
    name = forms.CharField(label='Composite',max_length=200,widget=forms.TextInput(attrs={"class": 'form-control'}))
    name_two =  forms.CharField(label='Composite',max_length=200,widget=forms.TextInput(attrs={"class": 'form-control'}))
    tensile_strength = forms.DecimalField(label='Tensile Strength',max_digits=19, decimal_places=10,widget=forms.TextInput(attrs={"class": 'form-control'}))
    young_modulus = forms.DecimalField(label='Young Modulus',max_digits=19, decimal_places=10,widget=forms.TextInput(attrs={"class": 'form-control'}))
    tensile_strength_two = forms.DecimalField(label='Tensile Strength',max_digits=19, decimal_places=10,widget=forms.TextInput(attrs={"class": 'form-control'}))
    young_modulus_two = forms.DecimalField(label='Young Modulus',max_digits=19, decimal_places=10,widget=forms.TextInput(attrs={"class": 'form-control'}))
# class Meta:
#         model = Composite
#         fields = '__all__'
#         widgets = {
#             "name": forms.TextInput(attrs={"class": 'form-control'}),
#             "tensile_strength":forms.NumberInput(attrs={"class": 'form-control'}),
#             "young_modulus":forms.NumberInput(attrs={"class": 'form-control'})
#         }