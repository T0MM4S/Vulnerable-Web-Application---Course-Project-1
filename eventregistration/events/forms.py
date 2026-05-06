from django import forms

from .models import Registration


class RegistrationForm(forms.ModelForm):
	class Meta:
		model = Registration
		fields = ['comments']
		widgets = {
			'comments': forms.Textarea(attrs={'rows': 4}),
		}
