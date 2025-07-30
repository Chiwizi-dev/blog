from django import forms
from .models import UserProfile
from datetime import date
from django.contrib.auth import get_user_model


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder":"Enter your Password"}))
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder":"Confirm Your Password"}))

    class Meta:
        model = get_user_model()
        fields = ("email", "user_name", "first_name", "last_name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs["placeholder"] = "Enter your Email address"
        self.fields["user_name"].label = "Username"
        self.fields["user_name"].widget.attrs["placeholder"] = "Enter a Username"
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter your First name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter your Last name"

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-fields"

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Password does not match!")
        return cleaned_data
    



class Edit_account_form(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "about"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field in self.fields:
                self.fields[field].widget.attrs["class"] = "form-fields"
    



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', "profile_picture", "address"]

        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                years=range(1900, date.today().year + 1)
            ),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field in self.fields:
                self.fields[field].widget.attrs["class"] = "form-fields"



class Edit_userprofile_form(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["date_of_birth", "profile_picture", "address"]

        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                years=range(1900, date.today().year + 1)
            ),
        }

        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                for field in self.fields:
                    self.fields[field].widget.attrs["class"] = "form-fields"