from django import forms

class UploadFile(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class UploadRecFile(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class DeleteFile(forms.Form):
    title = forms.CharField(max_length=50)