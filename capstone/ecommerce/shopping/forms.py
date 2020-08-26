from django import forms


class SignUpForm(forms.Form):
    GENDER = [
     ('Male', 'Male'),
     ('Female', 'Female'),
     ('Other', 'Other')
    ]

    full_name = forms.CharField(label="Full Name")
    password = forms.CharField(label="Password")
    gender = forms.ChoiceField(label="Gender", choices=GENDER)
    phone_number = forms.IntegerField(label="Phone Number")
    email = forms.EmailField(label="Email")

    birthday = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker4'
        })
    )


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title of Listing")
    desrc = forms.CharField(label="Description of Listing")
    category = forms.CharField(label="Category of Listing")
    quantity = forms.IntegerField(label="Quantity for Sale")
    image_file = forms.ImageField(label="Listing Images")
