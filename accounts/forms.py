from django import forms
from .models import User
from .validators import allow_only_images_validator, validate_numeric, validate_length, valid_email, \
    validate_csv_file_extension


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'username', 'required': 'required', 'class': 'form-control', 'id': 'username'}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'first name', 'required': 'required', 'class': 'form-control', 'id': 'first-name'}))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'last name', 'required': 'required', 'class': 'form-control', 'id': 'last-name'}))

    mobile_no = forms.Field(widget=forms.TextInput(
        attrs={'placeholder': 'mobile no', 'required': 'required', 'class': 'form-control',
               'id': 'phone-number', }), validators=[validate_numeric, validate_length], )



    email = forms.CharField(widget=forms.EmailInput(
        attrs={'placeholder': 'email', 'required': 'required', 'class': 'form-control',
               'id': 'email', }), validators=[valid_email], )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'personal_email', 'mobile_no','phone_no','address',
                  'address2','city','state','pin_code','region','is_active','role','region_manager','area_sales_manager'
            ,'som','ase','udm','rdm','nsm','nsdm','vp_sales','distributor','tier','britannia_program','sub_program',
                  'bdm']

    def clean(self):
        pass

class CSVUploadForm(forms.Form):
    ROLE_CHOICE = (
        ('', 'Select Profile'),
        ('Admin', 'Admin'),
        ('ASE', 'ASE'),
        ('ASM', 'ASM'),
        ('BDM', 'BDM'),
        ('Distributor', 'Distributor'),
        ('KYC', 'Approver'),
        ('NSDM', 'NSDM'),
        ('NSM', 'NSM'),
        ('Program Admin', 'Program Admin'),
        ('RDM', 'RDM'),

        ('Readonly Admin', 'Readonly Admin'),
        ('Retailer', 'Retailer'),

        ('RSM', 'RSM'),
        ('SOM', 'SOM'),
        ('UDM', 'UDM'),
        ('VP Sales', 'VP Sales'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICE,required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    csv_file = forms.FileField(
        validators=[validate_csv_file_extension],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

class UserInfoForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'first name', 'required': 'required', 'class': 'form-control', 'id': 'first-name'}))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'last name', 'required': 'required', 'class': 'form-control', 'id': 'last-name'}))

    phone_number = forms.Field(widget=forms.TextInput(
        attrs={'placeholder': 'phone number', 'required': 'required', 'class': 'form-control',
               'id': 'phone-number', }), validators=[validate_numeric, validate_length], )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
