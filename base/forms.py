from django import forms
from base.models import Institution, Building


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'
