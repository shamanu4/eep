# from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from base.models import Institution, Building, Component, ComponentType, FeatureType, Feature, MeterType, Meter, \
    MeterData, Rate, Receipt


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
    # date_from = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))

    class Meta:
        model = Building
        fields = '__all__'


class ComponentForm(forms.ModelForm):
    def __init__(self, building, *args, **kwargs):
        super(ComponentForm, self).__init__(*args, **kwargs)
        self.fields['building'] = forms.ModelChoiceField(
            queryset=building, label='Будівля', empty_label=None
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
    def __init__(self, component, *args, **kwargs):
        super(FeatureForm, self).__init__(*args, **kwargs)
        self.fields['component'] = forms.ModelChoiceField(
            queryset=component, label='Компонент', empty_label=None
        )

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
            queryset=institutions, label='Заклад', empty_label=None
        )
        self.fields['building'] = forms.ModelChoiceField(
            queryset=buildings, label='Будівля', empty_label=None
        )

    class Meta:
        model = Meter
        fields = '__all__'


class MeterDataForm(forms.ModelForm):
    def __init__(self, meter, *args, **kwargs):
        super(MeterDataForm, self).__init__(*args, **kwargs)
        self.fields['meter'] = forms.ModelChoiceField(
            queryset=meter, label='Лічильник', empty_label=None
        )

    class Meta:
        model = MeterData
        fields = '__all__'


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = '__all__'


class ReceiptForm(forms.ModelForm):
    def __init__(self, inst, build, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)
        self.fields['institution'] = forms.ModelChoiceField(
            queryset=inst, label='Заклад', empty_label=None
        )
        self.fields['building'] = forms.ModelChoiceField(
            queryset=build, label='Будівля', empty_label=None
        )

    class Meta:
        model = Receipt
        fields = '__all__'
