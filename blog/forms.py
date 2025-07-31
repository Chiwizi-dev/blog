from django import forms
from .models import Post




class CreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["category", "title", "summary", "content", "thumbnail"]



class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("thumbnail", "title", "summary", "content", "status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "edit_form"