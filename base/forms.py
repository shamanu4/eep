from django import forms
from guardian.shortcuts import get_objects_for_user
from base.models import Institution, Building, Component, ComponentType, FeatureType, Feature, MeterType, Meter, MeterData


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'


class BuildingForm(forms.ModelForm):
    def __init__(self, institutions, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)
        self.fields['institution'] = forms.ModelChoiceField(
            queryset=institutions, label='Заклад'
        )

    class Meta:
        model = Building
        fields = '__all__'


class ComponentForm(forms.ModelForm):
    def __init__(self, buildings, *args, **kwargs):
        super(ComponentForm, self).__init__(*args, **kwargs)
        self.fields['building'] = forms.ModelChoiceField(
            queryset=buildings, label='Будівля'
        )

    class Meta:
        model = Component
        fields = '__all__'


class ComponentTypeForm(forms.ModelForm):

    class Meta:
        model = ComponentType
        fields = '__all__'


class FeatureTypeForm(forms.ModelForm):
    class Meta:
        model = FeatureType
        fields = '__all__'


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = '__all__'


class MeterTypeForm(forms.ModelForm):
    class Meta:
        model = MeterType
        fields = '__all__'


class MeterForm(forms.ModelForm):
    def __init__(self, institutions, buildings, *args, **kwargs):
        super(MeterForm, self).__init__(*args, **kwargs)
        self.fields['institution'] = forms.ModelChoiceField(
            queryset=institutions, label='Заклад'
        )
        self.fields['building'] = forms.ModelChoiceField(
            queryset=buildings, label='Будівля'
        )

    class Meta:
        model = Meter
        fields = '__all__'


class MeterDataForm(forms.ModelForm):
    def __init__(self, meters, *args, **kwargs):
        super(MeterDataForm, self).__init__(*args, **kwargs)
        self.fields['meter'] = forms.ModelChoiceField(
            queryset=meters, label='Лічильник'
        )

    class Meta:
        model = MeterData
        fields = '__all__'
