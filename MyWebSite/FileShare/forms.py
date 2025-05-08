# MyWebSite/FileShare/forms.py
from django import forms
from .models import Files

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['files']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class FolderUploadForm(forms.Form):
    folder = forms.FileField(widget=forms.ClearableFileInput(attrs={'webkitdirectory': True, 'directory': True}))