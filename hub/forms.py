from django import forms

from .models import LeadRequest, NewsletterSubscriber


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ('email', 'first_name', 'company', 'goals')
        widgets = {'goals': forms.Textarea(attrs={'rows': 3})}


class LeadRequestForm(forms.ModelForm):
    class Meta:
        model = LeadRequest
        fields = ('name', 'email', 'instagram_handle', 'message')
        widgets = {'message': forms.Textarea(attrs={'rows': 4})}
