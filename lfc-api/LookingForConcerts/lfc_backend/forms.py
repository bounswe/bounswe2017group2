from django import forms

class ConcertImageForm(forms.Form):
    image = forms.FileField(label='Select a concert image')

class UserImageForm(forms.Form):
    image = forms.FileField(label='Select a user image')
