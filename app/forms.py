from django import forms
from accounts.models import Region
from accounts.validators import validate_csv_file_extension


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'status', 'state']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        if not status:
            self.add_error('status', 'Please select status.')
        return cleaned_data


class CSVUploadForm(forms.Form):
    ROLE_CHOICE = (
        ('', 'Select Profile'),
        ('Admin', 'Admin'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICE,required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    csv_file = forms.FileField(
        validators=[validate_csv_file_extension],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )