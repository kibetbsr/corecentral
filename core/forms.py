from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'you@example.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'What is this about?'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Write your message here...', 'rows': 5
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError('Please enter your full name.')
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError('Message is too short. Please tell us a bit more.')
        return message
