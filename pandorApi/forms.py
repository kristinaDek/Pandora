from django import forms
from .models import ImportantOccasionModel

class ImportantOccasionForm(forms.ModelForm):

    class Meta:
        model = ImportantOccasionModel
        # fields = '__all__'
        exclude = ['user']